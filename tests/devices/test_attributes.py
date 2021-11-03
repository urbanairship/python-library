import datetime
from time import time
import unittest

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
                airship=self.test_airship,
                attributes=[self.set_attribute],
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
