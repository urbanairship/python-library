import json
import mock
import unittest
import uuid

import requests

import urbanairship as ua
from tests import TEST_SECRET, TEST_KEY, TEST_TOKEN


class TestAirshipCore(unittest.TestCase):
    def test_airship_timeout(self):
        timeout_int = 50

        airship_timeout = ua.Airship(
            key=TEST_KEY, secret=TEST_SECRET, timeout=timeout_int
        )

        self.assertEqual(airship_timeout.timeout, timeout_int)

    def test_airship_timeout_exception(self):
        timeout_str = "50"

        with self.assertRaises(ValueError):
            ua.Airship(key=TEST_KEY, secret=TEST_SECRET, timeout=timeout_str)

    def test_airship_location(self):
        location = "eu"

        airship_eu = ua.Airship(key=TEST_KEY, secret=TEST_SECRET, location=location)

        self.assertEqual(airship_eu.location, location)

    def test_airship_location_exception(self):
        invalid_location = "xx"

        with self.assertRaises(ValueError):
            ua.Airship(key=TEST_KEY, secret=TEST_SECRET, location=invalid_location)

    def test_token_auth(self):
        test_airship = ua.Airship(key=TEST_KEY, token=TEST_TOKEN)

        self.assertEqual(TEST_TOKEN, test_airship.token)

    def test_no_secret_nor_token(self):
        with self.assertRaises(
            ValueError, msg="One of token or secret must be used, not both"
        ):
            ua.Airship(key=TEST_KEY)

    def test_both_secret_and_token(self):
        with self.assertRaises(
            ValueError, msg="Either token or secret must be included"
        ):
            ua.Airship(key=TEST_KEY, secret=TEST_SECRET, token=TEST_TOKEN)


class TestAirshipResponse(unittest.TestCase):
    test_channel = str(uuid.uuid4())
    airship = ua.Airship(TEST_KEY, TEST_SECRET)
    common_push = airship.create_push()
    common_push.device_types = ua.device_types("ios", "android", "amazon")
    common_push.audience = ua.channel(test_channel)
    common_push.notification = ua.notification(alert="testing")

    def test_unauthorized(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": False}).encode("utf-8")
            response.status_code = 401
            mock_request.return_value = response

            try:
                self.common_push.send()
            except Exception as e:
                self.assertIsInstance(ua.Unauthorized, e)

    def test_client_error(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": False}).encode("utf-8")
            response.status_code = 400
            mock_request.return_value = response

            try:
                r = self.common_push.send()
            except Exception as e:
                self.assertIsInstance(ua.AirshipFailure, e)
                self.assertEqual(r.status_code, 400)

    def test_server_error(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": False}).encode("utf-8")
            response.status_code = 500
            mock_request.return_value = response

            try:
                r = self.common_push.send()
            except Exception as e:
                self.assertIsInstance(ua.AirshipFailure, e)
                self.assertEqual(r.status_code, 500)
