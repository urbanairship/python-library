import json
import mock
import unittest

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestSMS(unittest.TestCase):
    def test_sms_channel_reg(self):
        sender = '12345'
        msisdn = '15035556789'
        channel_id = None

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
                'status': 'pending'
            }).encode('utf-8')
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            sms_obj.register()

            self.assertEqual(channel_id, sms_obj.channel_id)

    def test_sms_channel_reg_with_optin(self):
        sender = '12345'
        msisdn = '15035556789'
        channel_id = '59968b83-4e21-4e4a-85ce-25bb59a93993'
        opt_in_date = '2018-02-13T11:58:59'

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
                'channel_id': channel_id
            }).encode('utf-8')
            response.status_code = 201
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            sms_obj.register(opted_in=opt_in_date)

            self.assertEqual(channel_id, sms_obj.channel_id)

    def test_sms_opt_out(self):
        sender = '12345'
        msisdn = '15035556789'

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
            }).encode('utf-8')
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            r = sms_obj.opt_out()

            self.assertTrue(r.ok)

    def test_sms_uninstall(self):
        sender = '12345'
        msisdn = '15035556789'

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
            }).encode('utf-8')
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            r = sms_obj.uninstall()

            self.assertTrue(r.ok)

    def test_sms_lookup(self):
        sender = '12345'
        msisdn = '15035556789'

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                "ok": True,
                "channel": {
                    "channel_id": "84e36d69-873b-4ffe-81cd-e74c9f002057",
                    "device_type": "sms",
                    "installed": True,
                    "push_address": None,
                    "named_user_id": None,
                    "alias": None,
                    "tags": [],
                    "tag_groups": {
                        "ua_channel_type": [
                            "sms"
                        ],
                        "ua_sender_id": [
                            "12345"
                        ],
                        "ua_opt_in": [
                            "true"
                        ]
                    },
                    "created": "2018-04-27T22:06:21",
                    "opt_in": True,
                    "last_registration": "2018-05-14T19:51:38"
                }
            }).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            r = sms_obj.lookup()

            self.assertTrue(r.ok)
