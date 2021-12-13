import unittest
import json

import mock
from mock import Mock
import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestNamedUser(unittest.TestCase):
    def test_Named_User(self):
        ok_true = json.dumps({"ok": True}).encode("utf-8")

        associate_response = requests.Response()
        associate_response.status_code = 200
        associate_response._content = ok_true

        disassociate_response = requests.Response()
        disassociate_response._content = ok_true
        disassociate_response.status_code = 200

        lookup_response = requests.Response()
        lookup_response._content = json.dumps(
            {
                "ok": True,
                "named_user": {
                    "named_user_id": "name1",
                    "tags": {"group_name": ["tag1", "tag2"]},
                },
            }
        ).encode("utf-8")

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [
            associate_response,
            disassociate_response,
            lookup_response,
        ]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)

        nu = ua.NamedUser(airship, "name1")

        associate = nu.associate(channel_id="channel_id", device_type="ios")
        self.assertEqual(associate.status_code, 200)
        self.assertEqual(associate.ok, True)

        disassociate = nu.disassociate(channel_id="channel_id", device_type="ios")
        self.assertEqual(disassociate.status_code, 200)
        self.assertEqual(disassociate.ok, True)

        lookup = nu.lookup()

        self.assertEqual(lookup["ok"], True)
        self.assertEqual(
            lookup["named_user"],
            {"named_user_id": "name1", "tags": {"group_name": ["tag1", "tag2"]}},
        )

    def test_channel_associate_payload_property(self):
        named_user = ua.NamedUser(
            airship=ua.Airship(TEST_KEY, TEST_SECRET), named_user_id="cowboy_dan"
        )
        named_user.channel_id = "524bb82-8499-4ba5-b313-2157b1b1771f"
        named_user.device_type = "ios"

        self.assertEqual(
            named_user._channel_associate_payload,
            {
                "named_user_id": "cowboy_dan",
                "channel_id": "524bb82-8499-4ba5-b313-2157b1b1771f",
                "device_type": "ios",
            },
        )

    def test_email_associate_payload_property(self):
        named_user = ua.NamedUser(
            airship=ua.Airship(TEST_KEY, TEST_SECRET), named_user_id="cowboy_dan"
        )
        named_user.email_address = "major_player@cowboyscene.net"

        self.assertEqual(
            named_user._email_associate_payload,
            {
                "named_user_id": "cowboy_dan",
                "email_address": "major_player@cowboyscene.net",
            },
        )

    def test_named_user_uninstall_raises(self):
        with self.assertRaises(ValueError):
            ua.NamedUser.uninstall(
                airship=ua.Airship(TEST_KEY, TEST_SECRET),
                named_users="should_be_a_list",
            )

    def test_named_user_tag(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        nu = ua.NamedUser(airship, "named_user_id")

        self.assertRaises(
            ValueError,
            nu.tag,
            "tag_group_name",
            add={"group": "tag"},
            set={"group": "other_tag"},
        )

    def test_named_user_update_raises(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        nu = ua.NamedUser(airship, "named_user_id")

        with self.assertRaises(ValueError):
            nu.update()

    def test_named_user_attributes_raises(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        nu = ua.NamedUser(airship, "named_user_id")

        with self.assertRaises(ValueError):
            nu.attributes(
                attributes={"action": "set", "key": "type", "value": "not_a_list"}
            )


class TestNamedUserList(unittest.TestCase):
    def test_NamedUserlist_iteration(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "named_users": [
                        {"named_user_id": "name1"},
                        {"named_user_id": "name2"},
                        {"named_user_id": "name3"},
                    ]
                }
            ).encode("utf-8")
            mock_request.return_value = response

            name_list = ["name3", "name2", "name1"]
            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            named_user_list = ua.NamedUserList(airship)

            for a in named_user_list:
                self.assertEqual(a.named_user_id, name_list.pop())


class TestNamedUserTags(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.named_user_tags = ua.NamedUserTags(self.airship)
        self.mock_response = requests.Response()
        self.mock_response._content = json.dumps([{"ok": True}]).encode("utf-8")

        ua.Airship._request = mock.Mock()
        ua.Airship._request.side_effect = [self.mock_response]

    def test_set_audience(self):
        self.named_user_tags.set_audience(["user-1", "user-2"])

        self.assertEqual(
            self.named_user_tags.audience, {"named_user_id": ["user-1", "user-2"]}
        )

    def test_add(self):
        self.named_user_tags.set_audience(["user-1", "user-2"])
        self.named_user_tags.add("group1", ["tag1", "tag2", "tag3"])
        result = self.named_user_tags.send()

        self.assertEqual(result, [{"ok": True}])
