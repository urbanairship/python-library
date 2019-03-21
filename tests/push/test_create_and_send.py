import datetime
import unittest

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestCreateAndSend(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.test_sms_sender = '12345'
        self.test_sms_msisdns = ['15035556789', '15035556788', '15035556787']
        self.test_open_channel_addresses = [
            'bfecbb67-5352-4582-a95d-24e4760a3907',
            'bfecbb67-5352-4582-a95d-24e4760a3908',
            'bfecbb67-5352-4582-a95d-24e4760a3909'
        ]
        self.test_email_addresses = [
            'foo@urbanairship.com',
            'bar@urbanairship.com',
            'baz@urbanairship.com'
        ]
        self.test_optin_datestring = '2018-02-13T11:58:59'
        self.test_sms_objs = []
        self.test_open_channel_objs = []
        self. test_email_objs = []

        for msisdn in self.test_sms_msisdns:
            sms_obj = ua.Sms(
                airship=self.airship,
                sender=self.test_sms_sender,
                opted_in=self.test_optin_datestring,
                msisdn=msisdn)
            self.test_sms_objs.append(sms_obj)
        for address in self.test_open_channel_addresses:
            open_channel_obj = ua.OpenChannel(
                airship=self.airship
            )
            open_channel_obj.address = address
            open_channel_obj.open_platform = 'open::foo'
            self.test_open_channel_objs.append(open_channel_obj)
        for email in self.test_email_addresses:
            email_obj = ua.Email(
                airship=self.airship,
                address=email,
                commercial_opted_in=self.test_optin_datestring
            )
            self.test_email_objs.append(email_obj)

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
            cas.payload

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
            cas.payload

    def test_large_list(self):
        big_list = [x for x in range(1001)]

        with self.assertRaises(ValueError):
            ua.CreateAndSendPush(
                airship=self.airship,
                channels=big_list
            )

    def test_non_list_channels(self):
        fail_tuple = (x for x in range(5))

        with self.assertRaises(TypeError):
            ua.CreateAndSendPush(
                airship=self.airship,
                channels=fail_tuple
            )

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

    def test_open_channel_send(self):
        cas = ua.CreateAndSendPush(
            airship=self.airship,
            channels=self.test_open_channel_objs,
        )
        cas.notification = ua.notification(
            alert='test open channel'
        )
        cas.device_types = ua.device_types('open::foo')
        cas.campaigns = ua.campaigns(
            categories=['foo', 'bar', 'baz']
        )
        self.assertEqual(
            cas.payload,
            {
                'audience': {
                    'create_and_send': [
                        {
                            'ua_address': 'bfecbb67-5352-4582-a95d-24e4760a3907'
                        },
                        {
                            'ua_address': 'bfecbb67-5352-4582-a95d-24e4760a3908'
                        },
                        {
                            'ua_address': 'bfecbb67-5352-4582-a95d-24e4760a3909'
                        }
                    ]
                },
                'device_types': ['open::foo'],
                'notification': {
                    'alert': 'test open channel'
                },
                'campaigns': {
                    'categories': ['foo', 'bar', 'baz']
                }
            }
        )

    def test_email_send(self):
        cas = ua.CreateAndSendPush(
            airship=self.airship,
            channels=self.test_email_objs
        )
        cas.notification = ua.notification(
            email=ua.email(
                message_type='commercial',
                plaintext_body='this is an email',
                reply_to='foo@urbanairship.com',
                sender_address='bar@urbanairship.com',
                sender_name='test sender',
                subject='this is an email'
            )
        )
        cas.device_types = ua.device_types('email')
        cas.campaigns = ua.campaigns(
            categories=['email', 'fun']
        )
        self.assertEqual(
            cas.payload,
            {
                'audience': {
                    'create_and_send': [
                        {
                            'ua_address': 'foo@urbanairship.com',
                            'ua_commercial_opted_in': '2018-02-13T11:58:59'
                        },
                        {
                            'ua_address': 'bar@urbanairship.com',
                            'ua_commercial_opted_in': '2018-02-13T11:58:59'
                        },
                        {
                            'ua_address': 'baz@urbanairship.com',
                            'ua_commercial_opted_in': '2018-02-13T11:58:59'
                        }
                    ]
                },
                'device_types': ['email'],
                'notification': {
                    'email': {
                        'subject': 'this is an email',
                        'plaintext_body': 'this is an email',
                        'message_type': 'commercial',
                        'sender_name': 'test sender',
                        'sender_address': 'bar@urbanairship.com',
                        'reply_to': 'foo@urbanairship.com'
                    }
                },
                'campaigns': {
                    'categories': ['email', 'fun']
                }
            }
        )

    def test_scheduled_send(self):
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
        schedule = ua.ScheduledPush(airship=self.airship)
        schedule.name = 'test schedule name'
        schedule.push = cas
        schedule.schedule = ua.scheduled_time(
            datetime.datetime(2025, 10, 8, 12, 15)
            )
        self.assertEqual(
            schedule.payload,
            {
                'schedule': {
                    'scheduled_time': '2025-10-08T12:15:00'
                },
                'name': 'test schedule name',
                'push': {
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
            }
        )


class TestCreateAndSendInlineTemplate(unittest.TestCase):
    def setUp(self):
        pass

    def test_sms_inline_template(self):
        pass

    def test_open_inline_template(self):
        pass

    def test_email_open_inline_template(self):
        pass

    def test_template_fields_not_dict(self):
        pass
