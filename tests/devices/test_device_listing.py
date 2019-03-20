import json
import unittest
import mock
import requests
import datetime

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestDeviceListing(unittest.TestCase):
    def setUp(self):
        self.channel1 = '2ce7bb20-03a1-417d-bef5-61306e3755d7'
        self.channel2 = '4c3b6679-16f9-450a-9781-938cb3e9db7c'
        self.channel3 = 'aaabf77c-432e-4468-8b4a-0a173685e58f'
        self.push_address1 = '28A97947F08FF0E0026EF38D157E0B1777B8DDD33D3B16130679288CEED645AF'
        self.push_address2 = 'dBxM9bDfoBc:APA91bEVEmD6qDehBmYz7xHDwxuv9dYZN9iegJGUBUpV17P51JafpjYrCmSZQkJUkBuKKmizk0eXwxT3UT_gpReFs2aXnp3UdjJ_DhuH1DYBmw_HuOQjI0oklU8DWVr1aurIP2Q3K5We'
        self.push_address3 = None
        self.device_token1 = '0101F9929660BAD9FFF31A0B5FA32620FA988507DFFA52BD6C1C1F4783EDA2DB'
        self.device_token2 = '07AAFE44CD82C2F4E3FBAB8962A95B95F90A54857FB8532A155DE3510B481C13'
        self.apid1 = '00000000-0000-0000-0000-000000000000'
        self.apid2 = '11111111-1111-1111-1111-111111111111'

    def test_channel_listing(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "ok": "true",
                    "channels": [
                        {
                            "channel_id": "2ce7bb20-03a1-417d-bef5-61306e3755d7",
                            "device_type": "ios",
                            "installed": "true",
                            "opt_in": "true",
                            "background": "true",
                            "push_address": "28A97947F08FF0E0026EF38D157E0B1777B8DDD33D3B16130679288CEED645AF",
                            "created": "2016-08-17T23:29:52",
                            "last_registration": "2016-08-18T17:57:31",
                            "named_user_id": "null",
                            "alias": "null",
                            "tags": [],
                            "tag_groups": {
                                "ua_background_enabled": [
                                    "true"
                                ],
                                "ua_ios_app_version": [
                                    "1.0"
                                ],
                                "timezone": [
                                    "America/Los_Angeles"
                                ],
                                "ua_locale_country": [
                                    "US"
                                ],
                                "ua_locale_language": [
                                    "en"
                                ],
                                "ua_ios_model": [
                                    "iPad2,5"
                                ],
                                "ua_ios_sdk_version": [
                                    "7.2.X"
                                ],
                                "ua_ios_version": [
                                    "9.3.X"
                                ],
                                "ua_opt_in": [
                                    "true"
                                ],
                                "ua_location_enabled": [
                                    "false"
                                ]
                            },
                            "ios": {
                                "badge": 0,
                                "quiettime": {
                                    "start": "null",
                                    "end": "null"
                                },
                                "tz": "null"
                            }
                        },
                        {
                            "channel_id": "4c3b6679-16f9-450a-9781-938cb3e9db7c",
                            "device_type": "android",
                            "installed": "false",
                            "opt_in": "false",
                            "background": "false",
                            "push_address": "dBxM9bDfoBc:APA91bEVEmD6qDehBmYz7xHDwxuv9dYZN9iegJGUBUpV17P51JafpjYrCmSZQkJUkBuKKmizk0eXwxT3UT_gpReFs2aXnp3UdjJ_DhuH1DYBmw_HuOQjI0oklU8DWVr1aurIP2Q3K5We",
                            'created': 'None',
                            "last_registration": "2016-08-22T17:20:27",
                            "named_user_id": "null",
                            "alias": "null",
                            "tags": [],
                            "tag_groups": {
                                "ua_background_enabled": [
                                    "false"
                                ],
                                "ua_opt_in": [
                                    "false"
                                ]
                            }
                        },
                        {
                            "channel_id": "aaabf77c-432e-4468-8b4a-0a173685e58f",
                            "device_type": "open",
                            "installed": "true",
                            "named_user_id": "cat",
                            "alias": "null",
                            "tags": ["likes-cats", "likes-demos"],
                            "tag_groups": {
                                "timezone": ["America/Los_Angeles"],
                                "ua_locale_country": ["US"],
                                "ua_locale_language": ["en"],
                                "ua_opt_in": ["true"]
                            },
                            "created": "2017-08-11T19:17:33",
                            "address": "+1 8008675309",
                            "opt_in": "true",
                            "open": {
                                "open_platform_name": "sms",
                                "identifiers": {
                                    "likes-spam": "false",
                                    "likes-cats": "very true"
                                }
                            },
                            "last_registration": "2017-08-11T19:17:33"
                        }
                    ]
                }
            ).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)

            channel_responses = []

            for channel in ua.ChannelList(airship):
                channel_responses.append(channel)

            self.assertEquals(channel_responses[0].channel_id, self.channel1)
            self.assertEquals(channel_responses[1].channel_id, self.channel2)
            self.assertEquals(channel_responses[2].channel_id, self.channel3)

            self.assertEquals(
                channel_responses[0].push_address, self.push_address1
            )
            self.assertEquals(
                channel_responses[1].push_address, self.push_address2
            )
            self.assertEquals(
                channel_responses[2].push_address, self.push_address3
            )

            self.assertEquals(channel_responses[0].device_type, 'ios')
            self.assertEquals(channel_responses[1].device_type, 'android')
            self.assertEquals(channel_responses[2].device_type, 'open')

            self.assertEquals(
                channel_responses[0].created,
                datetime.datetime.strptime(
                    '2016-08-17T23:29:52',
                    '%Y-%m-%dT%H:%M:%S'
                )
            )
            self.assertEquals(channel_responses[1].created, 'UNKNOWN')
            self.assertEquals(
                channel_responses[2].created,
                datetime.datetime.strptime(
                    '2017-08-11T19:17:33',
                    '%Y-%m-%dT%H:%M:%S'
                )
            )

    def test_device_token_listing(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "next_page": "https://go.urbanairship.com/api/device_tokens/?start=07AAFE44CD82C2F4E3FBAB8962A95B95F90A54857FB8532A155DE3510B481C13&limit=2",
                    "device_tokens_count": 87,
                    "active_device_tokens_count": 37,
                    "device_tokens": [
                        {
                            "tags": [],
                            "alias": None,
                            "active": False,
                            "created": "2013-07-17 21:17:42",
                            "device_token": "0101F9929660BAD9FFF31A0B5FA32620FA988507DFFA52BD6C1C1F4783EDA2DB"
                        },
                        {
                            "tags": ["tag1", "tag2"],
                            "alias": "an_alias",
                            "active": True,
                            "created": "2016-02-05 22:55:54",
                            "device_token": "07AAFE44CD82C2F4E3FBAB8962A95B95F90A54857FB8532A155DE3510B481C13",
                        }
                    ]
                }
            ).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)

            dt_responses = []

            for dt in ua.DeviceTokenList(airship):
                dt_responses.append(dt)

            self.assertEquals(dt_responses[0].device_token, self.device_token1)
            self.assertEquals(dt_responses[1].device_token, self.device_token2)
            self.assertEquals(dt_responses[0].alias, None)
            self.assertEquals(dt_responses[1].alias, 'an_alias')
            self.assertEquals(dt_responses[0].active, False)
            self.assertEquals(dt_responses[1].active, True)
            self.assertEquals(
                dt_responses[0].created,
                datetime.datetime.strptime(
                        '2013-07-17 21:17:42', '%Y-%m-%d %H:%M:%S')
            )
            self.assertEquals(
                dt_responses[1].created,
                datetime.datetime.strptime(
                        '2016-02-05 22:55:54', '%Y-%m-%d %H:%M:%S')
            )
            self.assertListEqual(dt_responses[0].tags, [])
            self.assertListEqual(dt_responses[1].tags, ['tag1', 'tag2'])

    def test_apid_listing(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "next_page": "https://go.urbanairship.com/api/apids/?start=11111111-1111-1111-1111-111111111111&limit=2000",
                    "apids": [
                        {
                            "tags": [],
                            "alias": None,
                            "active": False,
                            "created": "2015-04-25 23:01:53",
                            "apid": "00000000-0000-0000-0000-000000000000",
                        },
                        {
                            "tags": ["tag1"],
                            "alias": "alias1",
                            "active": True,
                            "created": "2013-01-25 00:55:06",
                            "apid": "11111111-1111-1111-1111-111111111111"
                        }
                    ]
                }
            ).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)

            apid_responses = []

            for apid in ua.APIDList(airship):
                apid_responses.append(apid)

            self.assertEquals(apid_responses[0].apid, self.apid1)
            self.assertEquals(apid_responses[1].apid, self.apid2)
            self.assertEquals(apid_responses[0].active, False)
            self.assertEquals(apid_responses[1].active, True)
            self.assertEquals(apid_responses[0].alias, None)
            self.assertEquals(apid_responses[1].alias, 'alias1')
            self.assertEquals(
                apid_responses[0].created,
                datetime.datetime.strptime(
                        '2015-04-25 23:01:53', '%Y-%m-%d %H:%M:%S')
            )
            self.assertEquals(
                apid_responses[1].created,
                datetime.datetime.strptime(
                        '2013-01-25 00:55:06', '%Y-%m-%d %H:%M:%S')
            )
            self.assertListEqual(apid_responses[0].tags, [])
            self.assertListEqual(apid_responses[1].tags, ['tag1'])
