import json
import unittest
import mock
import requests
import datetime
import urbanairship as ua


class TestDeviceListing(unittest.TestCase):
    def setUp(self):
        self.channel1 = '2ce7bb20-03a1-417d-bef5-61306e3755d7'
        self.channel2 = '4c3b6679-16f9-450a-9781-938cb3e9db7c'
        self.push_address1 = '28A97947F08FF0E0026EF38D157E0B1777B8DDD33D3B16130679288CEED645AF'
        self.push_address2 = 'dBxM9bDfoBc:APA91bEVEmD6qDehBmYz7xHDwxuv9dYZN9iegJGUBUpV17P51JafpjYrCmSZQkJUkBuKKmizk0eXwxT3UT_gpReFs2aXnp3UdjJ_DhuH1DYBmw_HuOQjI0oklU8DWVr1aurIP2Q3K5We'

    def test_channel_listing(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "ok":"true",
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
                            'created': 'randomthing',
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
                        }
                    ]
                }
            ).encode('utf-8')
            
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')

            channel_responses = []

            for channel in ua.ChannelList(airship):
                channel_responses.append(channel)

            self.assertEquals(channel_responses[0].channel_id, self.channel1)
            self.assertEquals(channel_responses[1].channel_id, self.channel2)

            self.assertEquals(channel_responses[0].push_address, self.push_address1)
            self.assertEquals(channel_responses[1].push_address, self.push_address2)

            self.assertEquals(channel_responses[0].device_type, 'ios')
            self.assertEquals(channel_responses[1].device_type, 'android')

            self.assertEquals(channel_responses[0].created, '2016-08-17T23:29:52')
            self.assertEquals(channel_responses[1].created, 'UNKNOWN')

    
