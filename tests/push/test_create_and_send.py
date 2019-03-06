import datetime
import json
import unittest

import mock
import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestCreateAndSend(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.test_sms_sender = '12345'
        self.test_sms_msisdns = ['15035556789', '15035556788', '15035556787']
        self.test_optin_datestring = '2018-02-13T11:58:59'
        self.test_sms_objs = []
        for msisdn in self.test_sms_msisdns:
            sms_obj = ua.Sms(
                airship=self.airship, 
                sender=self.test_sms_sender, 
                opted_in=self.test_optin_datestring,
                msisdn=msisdn)
            self.test_sms_objs.append(sms_obj)

    def test_mixed_platforms(self):
        email_channel = ua.Email(
            self.airship,
            address='testing@urbanairship.com',
            commercial_opted_in=self.test_optin_datestring)
        mixed_channels = self.test_sms_objs
        mixed_channels.append(email_channel)
        
        cas = ua.CreateAndSendPush(
            self.airship,
            channels=mixed_channels
        )
        cas.device_types = ua.device_types('sms')
        cas.notification = ua.notification(alert='test sms')

        with self.assertRaises(TypeError):
            payload = cas.payload

    def test_multiple_device_types(self):
        cas = ua.CreateAndSendPush(
            self.airship,
            channels=self.test_sms_objs
        )
        with self.assertRaises(ValueError):
            cas.device_types = ua.device_types('sms', 'ios')

    def test_sms_without_optin(self):
        no_opt_in_sms = ua.Sms(
            airship=self.airship,
            sender=self.test_sms_sender,
            msisdn=self.test_sms_msisdns[0]
        )
        channels = self.test_sms_objs
        channels.append(no_opt_in_sms)
        
        cas = ua.CreateAndSendPush(
            self.airship,
            channels=channels
        )
        cas.device_types = ua.device_types('sms')
        cas.notification = ua.notification(alert='test sms')

        with self.assertRaises(ValueError):
            payload = cas.payload

    def test_sms_send(self):
        cas = ua.CreateAndSendPush(
            airship=self.airship,
            channels=self.test_sms_objs
        )
        cas.notification = ua.notification(
            alert='test sms'
        )
        cas.device_types = ua.device_types('sms')
        cas.campaigns = ua.campaigns(
            categories=['sms', 'offers']
        )
        self.assertEqual(
            cas.payload,
            {
                'audience': {
                        'create_and_send': [
                        {
                            'ua_msisdn': '15035556789',
                            'ua_sender': '12345',
                            'ua_opted_in': '2018-02-13T11:58:59'
                        },
                        {
                            'ua_msisdn': '15035556788',
                            'ua_sender': '12345',
                            'ua_opted_in': '2018-02-13T11:58:59'
                        },
                        {
                            'ua_msisdn': '15035556787',
                            'ua_sender': '12345',
                            'ua_opted_in': '2018-02-13T11:58:59'
                        },
                    ]
                },
                'notification': {'alert': 'test sms'},
                'device_types': ['sms'],
                'campaigns': {
                    'categories': ['sms', 'offers']
                }
            }
        )