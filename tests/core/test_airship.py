import json
import unittest
import uuid

import mock
import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


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

    def test_airship_retry(self):
        retry_int = 5

        airship_w_retry = ua.Airship(TEST_KEY, TEST_SECRET, retries=retry_int)

        self.assertEqual(retry_int, airship_w_retry.retries)

    def test_airship_location(self):
        location = "eu"

        airship_eu = ua.Airship(key=TEST_KEY, secret=TEST_SECRET, location=location)

        self.assertEqual(airship_eu.location, location)

    def test_airship_location_exception(self):
        invalid_location = "xx"

        with self.assertRaises(ValueError):
            ua.Airship(key=TEST_KEY, secret=TEST_SECRET, location=invalid_location)


class TestAirshipResponse(unittest.TestCase):
    test_channel = str(uuid.uuid4())
    airship = ua.Airship(TEST_KEY, TEST_SECRET)
    common_push = ua.Push(airship)
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
                self.common_push.send()
            except ua.AirshipFailure as e:
                self.assertIsInstance(ua.AirshipFailure, e)

    def test_server_error(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": False}).encode("utf-8")
            response.status_code = 500
            mock_request.return_value = response

            try:
                self.common_push.send()
            except ua.AirshipFailure as e:
                self.assertIsInstance(ua.AirshipFailure, e)
