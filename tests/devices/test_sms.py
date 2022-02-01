from datetime import datetime
import json
import mock
import unittest

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET, TEST_TOKEN


class TestSMS(unittest.TestCase):
    def test_sms_channel_reg(self):
        sender = "12345"
        msisdn = "15035556789"
        channel_id = None

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True, "status": "pending"}).encode(
                "utf-8"
            )
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            sms_obj.register()

            self.assertEqual(channel_id, sms_obj.channel_id)

    def test_sms_channel_reg_with_optin(self):
        sender = "12345"
        msisdn = "15035556789"
        channel_id = "59968b83-4e21-4e4a-85ce-25bb59a93993"
        opt_in_date = "2018-02-13T11:58:59"

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {"ok": True, "channel_id": channel_id}
            ).encode("utf-8")
            response.status_code = 201
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            sms_obj.register(opted_in=opt_in_date)

            self.assertEqual(channel_id, sms_obj.channel_id)

    def test_sms_opt_out(self):
        sender = "12345"
        msisdn = "15035556789"

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("utf-8")
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            r = sms_obj.opt_out()

            self.assertTrue(r.ok)

    def test_sms_uninstall(self):
        sender = "12345"
        msisdn = "15035556789"

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True}).encode("utf-8")
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            r = sms_obj.uninstall()

            self.assertTrue(r.ok)

    def test_sms_registration_payload_property(self):
        sms = ua.Sms(
            airship=ua.Airship(TEST_KEY, TEST_SECRET),
            sender="12345",
            msisdn="15035556789",
            opted_in="2018-02-13T11:58:59",
            locale_country="us",
            locale_language="en",
            timezone="America/Los_Angeles",
        )

        self.assertEqual(
            sms._registration_payload,
            {
                "sender": "12345",
                "msisdn": "15035556789",
                "locale_language": "en",
                "locale_country": "us",
                "timezone": "America/Los_Angeles",
                "opted_in": "2018-02-13T11:58:59",
            },
        )

    def test_sms_lookup(self):
        sender = "12345"
        msisdn = "15035556789"

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
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
                            "ua_channel_type": ["sms"],
                            "ua_sender_id": ["12345"],
                            "ua_opt_in": ["true"],
                        },
                        "created": "2018-04-27T22:06:21",
                        "opt_in": True,
                        "last_registration": "2018-05-14T19:51:38",
                    },
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sms_obj = ua.Sms(airship, sender=sender, msisdn=msisdn)

            r = sms_obj.lookup()

            self.assertTrue(r.ok)


class TestSmsKeywordInteraction(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.sender_ids = ["12345", "09876"]
        self.msisdn = "15035556789"
        self.keyword = "from_a_motel_six"
        self.timestamp = datetime(2014, 10, 8, 12, 0, 0)
        self.interaction = ua.KeywordInteraction(
            airship=self.airship,
            keyword=self.keyword,
            msisdn=self.msisdn,
            sender_ids=self.sender_ids,
            timestamp=self.timestamp,
        )

    def test_payload(self):
        self.assertEqual(
            self.interaction.payload,
            {
                "keyword": self.keyword,
                "sender_ids": self.sender_ids,
                "timestamp": "2014-10-08T12:00:00",
            },
        )

    def test_url(self):
        self.assertEqual(
            self.interaction.url,
            "https://go.urbanairship.com/api/sms/15035556789/keywords",
        )


class TestSmsCustomResponse(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = 2000
        airship = ua.Airship(key=TEST_KEY, token=TEST_TOKEN)
        self.mo_id = "886f53d4-3e0f-46d7-930e-c2792dac6e0a"
        self.custom_response = ua.SmsCustomResponse(
            airship=airship,
            mobile_originated_id=self.mo_id,
        )

    def test_mms_payload(self):
        self.custom_response.mms = ua.mms(
            fallback_text="mms alert",
            url="http://www.airship.com",
            content_type="image/gif",
            content_length=12345,
            shorten_links=True,
        )

        self.assertEqual(
            self.custom_response._payload,
            {
                "mobile_originated_id": self.mo_id,
                "mms": {
                    "fallback_text": "mms alert",
                    "slides": [
                        {
                            "media": {
                                "content_type": "image/gif",
                                "url": "http://www.airship.com",
                                "content_length": 12345,
                            }
                        }
                    ],
                    "shorten_links": True,
                },
            },
        )

    def test_sms_payload(self):
        self.custom_response.sms = ua.sms(alert="sms alert", shorten_links=False)

        self.assertEqual(
            self.custom_response._payload,
            {
                "sms": {"alert": "sms alert", "shorten_links": False},
                "mobile_originated_id": self.mo_id,
            },
        )

    def test_neither_payload_raises(self):
        with self.assertRaises(ValueError, msg="One of mms or sms must be set."):
            self.custom_response._payload

    def test_both_payloads_raises(self):
        self.custom_response.sms = ua.sms(alert="test_alert")
        self.custom_response.mms = ua.mms(
            content_length=12345,
            content_type="image/png",
            fallback_text="test mms",
            url="url",
        )

        with self.assertRaises(ValueError, msg="Cannot use both mms and sms."):
            self.custom_response._payload
