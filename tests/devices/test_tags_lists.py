import json
import unittest

import mock
import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestTagLists(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(key=TEST_KEY, secret=TEST_SECRET)
        self.list_name = "test_tag_list"
        self.description = "a list of some tags"
        self.extra = {"key": "value"}
        self.file_path = "tests/data/tag_list.csv"
        self.tag_dict = {"group_name": ["tag1", "tag2"]}
        self.tag_list = ua.TagList(
            airship=self.airship,
            list_name=self.list_name,
            description=self.description,
            extra=self.extra,
            add_tags=self.tag_dict,
            remove_tags=self.tag_dict,
            set_tags=self.tag_dict,
        )

    def test_create(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("UTF-8")
            mock_request.return_value = response

            result = self.tag_list.create()

            self.assertEqual(result.json(), {"ok": True})

    def test_create_payload_property(self):
        self.assertEqual(
            self.tag_list._create_payload,
            {
                "name": self.list_name,
                "description": self.description,
                "extra": self.extra,
                "add": self.tag_dict,
                "remove": self.tag_dict,
                "set": self.tag_dict,
            },
        )

    def test_upload(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("UTF-8")
            mock_request.return_value = response

            result = self.tag_list.upload(file_path=self.file_path)

            self.assertEqual(result.json(), {"ok": True})

    def test_get_errors(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("UTF-8")
            mock_request.return_value = response

            result = self.tag_list.get_errors()

            self.assertEqual(result.json(), {"ok": True})

    def test_list(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("UTF-8")
            mock_request.return_value = response

            result = ua.TagList.list(airship=self.airship)

            self.assertEqual(result.json(), {"ok": True})
