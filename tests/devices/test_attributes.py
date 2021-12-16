import datetime
import unittest
import mock
import json

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestAttribute(unittest.TestCase):
    def setUp(self):
        self.test_time = datetime.datetime.utcnow()
        self.test_time_str = self.test_time.replace(microsecond=0).isoformat()

    def test_set_attribute(self):
        a = ua.Attribute(
            action="set", key="test_key", value="test_value", timestamp=self.test_time
        )

        self.assertEqual(
            a.payload,
            {
                "action": "set",
                "key": "test_key",
                "value": "test_value",
                "timestamp": self.test_time_str,
            },
        )

    def test_remove_attribute(self):
        a = ua.Attribute(
            action="remove",
            key="test_key",
            value="test_value",
            timestamp=self.test_time,
        )

        self.assertEqual(
            a.payload,
            {
                "action": "remove",
                "key": "test_key",
                "value": "test_value",
                "timestamp": self.test_time_str,
            },
        )

    def test_no_value_with_set(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.Attribute(action="set", key="test_key")

            self.assertEqual(
                err_ctx.message, "A value must be included with 'set' actions"
            )

    def test_str_timestamp(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.Attribute(
                action="set",
                key="test_key",
                value="test_value",
                timestamp=self.test_time_str,
            )

            self.assertEqual(
                err_ctx.message, "timestamp must be a datetime.datetime object"
            )

    def test_incorrect_action(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.Attribute(
                action="incorrect",
                key="test_key",
                value="test_value",
                timestamp=self.test_time,
            )
            self.assertEqual(err_ctx.message, "Action must be one of 'set' or 'remove'")


class TestModifyAttributes(unittest.TestCase):
    def setUp(self):
        self.set_attribute = ua.Attribute(
            action="set", key="test_key", value="test_value"
        )
        self.remove_attribute = ua.Attribute(
            action="remove", key="test_key", value="test_value"
        )
        self.test_channel = "c9c162d0-2c17-486b-938d-7b3eed5d8793"
        self.test_named_user = ua.named_user("my_cool_named_user")
        self.test_airship = ua.Airship(TEST_KEY, TEST_SECRET)

    def test_channel_payload(self):
        m = ua.ModifyAttributes(
            airship=self.test_airship,
            attributes=[self.set_attribute, self.remove_attribute],
            channel=self.test_channel,
        )
        self.assertEqual(
            m.payload,
            {
                "attributes": [
                    {"action": "set", "key": "test_key", "value": "test_value"},
                    {"action": "remove", "key": "test_key", "value": "test_value"},
                ],
                "audience": {"channel": [self.test_channel]},
            },
        )

    def test_named_user_payload(self):
        m = ua.ModifyAttributes(
            airship=self.test_airship,
            attributes=[self.set_attribute, self.remove_attribute],
            named_user=self.test_named_user,
        )
        self.assertEqual(
            m.payload,
            {
                "attributes": [
                    {"action": "set", "key": "test_key", "value": "test_value"},
                    {"action": "remove", "key": "test_key", "value": "test_value"},
                ],
                "audience": {"named_user_id": [self.test_named_user]},
            },
        )

    def test_attribute_alone(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.ModifyAttributes(
                airship=self.test_airship,
                attributes=self.set_attribute,
                channel=self.test_channel,
            )

            self.assertEqual(
                err_ctx.message, "attributes must be a list of Attribute objects"
            )

    def test_no_devices(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.ModifyAttributes(
                airship=self.test_airship, attributes=[self.set_attribute]
            )

            self.assertEqual(
                err_ctx.message, "Either channel or named_user must be included"
            )

    def test_both_devices(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.ModifyAttributes(
                airship=self.test_airship,
                attributes=[self.set_attribute],
                channel=self.test_channel,
                named_user=self.test_named_user,
            )

            self.assertEqual(
                err_ctx.message,
                "Either channel or named_user must be included, not both",
            )


class TestAttributeList(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.list_name = "my_test_list"
        self.description = "this is my cool list"
        self.extra = {"key": "value"}
        self.file_path = "tests/data/attribute_list.csv"
        self.attr_list = ua.AttributeList(
            airship=self.airship,
            list_name=self.list_name,
            description=self.description,
            extra=self.extra,
        )

    def test_create(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("UTF-8")
            mock_request.return_value = response

            result = self.attr_list.create()

            self.assertEqual(result.json(), {"ok": True})

    def test_upload(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("UTF-8")
            mock_request.return_value = response

            result = self.attr_list.upload(file_path=self.file_path)

            self.assertEqual(result.json(), {"ok": True})

    def test_create_payload_property(self):
        self.assertEqual(
            self.attr_list._create_payload,
            {
                "name": self.list_name,
                "description": self.description,
                "extra": self.extra,
            },
        )
