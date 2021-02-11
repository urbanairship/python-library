import json
import mock
import unittest
import uuid

import requests

import urbanairship as ua
from tests import TEST_SECRET, TEST_KEY


class TestAirshipResponse(unittest.TestCase):
    test_channel = str(uuid.uuid4())
    airship = ua.Airship(TEST_KEY, TEST_SECRET)
    common_push = airship.create_push()
    common_push.device_types = ua.device_types('ios', 'android', 'amazon')
    common_push.audience = ua.channel(test_channel)
    common_push.notification = ua.notification(alert='testing')

    def test_unauthorized(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': False
            }).encode('utf-8')
            response.status_code = 401
            mock_request.return_value = response

            try:
                self.common_push.send()
            except Exception as e:
                self.assertIsInstance(ua.Unauthorized, e)

    def test_client_error(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': False
            }).encode('utf-8')
            response.status_code = 400
            mock_request.return_value = response

            try:
                r = self.common_push.send()
            except Exception as e:
                self.assertIsInstance(ua.AirshipFailure, e)
                self.assertEqual(r.status_code, 400)

    def test_server_error(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': False
            }).encode('utf-8')
            response.status_code = 500
            mock_request.return_value = response

            try:
                r = self.common_push.send()
            except Exception as e:
                self.assertIsInstance(ua.AirshipFailure, e)
                self.assertEqual(r.status_code, 500)
