import datetime
import mock
import unittest
import json

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET
from urbanairship.push import audience


class TestSubscriptionList(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.ios_channel = ua.ios_channel("b8f9b663-0a3b-cf45-587a-be880946e881")

    def test_list_subscribe(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("utf-8")
            mock_request.return_value = response

            sub_list = ua.SubscriptionList(airship=self.airship, list_id="test_list")

            results = sub_list.subscribe(audience=self.ios_channel)

            self.assertEqual(results.json(), {"ok": True})

    def test_list_unsubscribe(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("utf-8")
            mock_request.return_value = response

            sub_list = ua.SubscriptionList(airship=self.airship, list_id="test_list")

            results = sub_list.unsubscribe(audience=self.ios_channel)

            self.assertEqual(results.json(), {"ok": True})
