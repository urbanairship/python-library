import json
import unittest

import mock
import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestABTest(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(key=TEST_KEY, secret=TEST_SECRET)
        self.ab_test = ua.ABTest(self.airship)
        self.experiment_id = "f0c975e4-c01a-436b-92a0-2a360f87b211"

    def test_delete(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("UTF-8")
            mock_request.return_value = response

            result = self.ab_test.delete(experiment_id=self.experiment_id)

            self.assertEqual(result.json(), {"ok": True})
            called_url = mock_request.call_args[0][2]
            self.assertNotIn("//", called_url.replace("https://", ""))
            self.assertTrue(called_url.endswith(f"experiments/scheduled/{self.experiment_id}"))

    def test_lookup(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("UTF-8")
            mock_request.return_value = response

            result = self.ab_test.lookup(experiment_id=self.experiment_id)

            self.assertEqual(result.json(), {"ok": True})
            called_url = mock_request.call_args[0][2]
            self.assertNotIn("//", called_url.replace("https://", ""))
            self.assertTrue(called_url.endswith(f"experiments/{self.experiment_id}"))
