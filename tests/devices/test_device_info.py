import json
import unittest
import mock
import requests
import datetime
import urbanairship as ua


class TestDeviceInfo(unittest.TestCase):
    def test_channel_list(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'channels': [
                        {'channel_id': '0492662a-1b52-4343-a1f9-c6b0c72931c0'},
                        {'channel_id': 'd95ceae2-85cb-41b7-a87d-09c9b3ce4051'},
                        {'channel_id': 'f10cf38c-3fbd-47e8-a4aa-43cf91d80ba1'}
                    ]
                }
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            url = ('https://go.urbanairship.com/api/channels/'
                   '0492662a-1b52-4343-a1f9-c6b0c72931c0')

            airship = ua.Airship('key', 'secret')
            channel_list = ua.ChannelList(airship, url)
            channel_id_list = []

            for channel in channel_list:
                channel_id_list.append(channel.channel_id)

            self.assertEqual(
                channel_id_list[0],
                '0492662a-1b52-4343-a1f9-c6b0c72931c0'
            )
            self.assertEqual(
                channel_id_list[1],
                'd95ceae2-85cb-41b7-a87d-09c9b3ce4051'
            )
            self.assertEqual(
                channel_id_list[2],
                'f10cf38c-3fbd-47e8-a4aa-43cf91d80ba1'
            )

    def test_channel_lookup(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'channel': {
                        'channel_id': '0492662a-1b52-4343-a1f9-c6b0c72931c0',
                        'device_type': 'ios',
                        'installed': 'false',
                        'opt_in': 'false',
                        'background': 'false',
                        'push_address': '3C0590EBCC11618723B3D4C8AA60BCFB6',
                        'created': '2014-04-17T23:35:15',
                        'last_registration': '2014-08-11T20:47:28',
                        'alias': 'null',
                        'tags': ['test_tag'],
                        'ios': {
                            'badge': 1,
                            'quiettime': {
                                'start': 'null',
                                'end': 'null'
                            },
                            'tz': 'null',
                        }
                    }
                }
            ).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            channel_id = '0492662a-1b52-4343-a1f9-c6b0c72931c0'
            channel_lookup = ua.ChannelInfo.lookup(airship, channel_id)

            date_created = (
                datetime.datetime.strptime(
                    '2014-04-17T23:35:15',
                    '%Y-%m-%dT%H:%M:%S'
                )
            )
            last_registration_date = (
                datetime.datetime.strptime(
                    '2014-08-11T20:47:28',
                    '%Y-%m-%dT%H:%M:%S'
                )
            )

            self.assertEqual(channel_lookup.channel_id, channel_id)
            self.assertEqual(channel_lookup.device_type, 'ios')
            self.assertEqual(channel_lookup.installed, 'false')
            self.assertEqual(channel_lookup.opt_in, 'false')
            self.assertEqual(channel_lookup.background, 'false')
            self.assertEqual(channel_lookup.alias, 'null')
            self.assertEqual(channel_lookup.tags, ['test_tag'])
            self.assertEqual(channel_lookup.created, date_created)
            self.assertEqual(
                channel_lookup.push_address,
                '3C0590EBCC11618723B3D4C8AA60BCFB6'
            )
            self.assertEqual(
                channel_lookup.last_registration,
                last_registration_date
            )
            self.assertEqual(
                channel_lookup.ios,
                {
                    'badge': 1,
                    'quiettime': {'start': 'null', 'end': 'null'},
                    'tz': 'null'
                }
            )

    def test_device_token_feedback(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps([
                {
                    'alias': None,
                    'device_token': ('4D95CB349F95ADEBE05F0A71B5F5B62D'
                                     '0F696667454DA60CD55282F67321710C'),
                    'marked_inactive_on': '2014-12-16 20:21:42'
                }
            ]).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            feedback = ua.Feedback.device_token(
                airship,
                datetime.datetime(2014, 11, 22)
            )
            date = datetime.datetime.strptime('2014-12-16 20:21:42',
                                              '%Y-%m-%d %H:%M:%S')

            self.assertEqual(
                feedback,
                [
                    {
                        'alias': None,
                        'device_token': ('4D95CB349F95ADEBE05F0A71B5F5B62D'
                                         '0F696667454DA60CD55282F67321710C'),
                        'marked_inactive_on': date
                    }
                ]
            )
            mock_request.assert_called_with(
                method='GET',
                body='',
                url='https://go.urbanairship.com/api/device_tokens/feedback/',
                version=3,
                params={'since': '2014-11-22T00:00:00'}
            )

    def test_apid_feedback(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps([
                {
                    'alias': None,
                    'apid': '80242a4c-d870-4fce-b0c3-724c865cfbfe',
                    'gcm_registration_id': 'null',
                    'marked_inactive_on': '2014-12-16 20:21:42'
                }
            ]).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            feedback = ua.Feedback.apid(
                airship,
                datetime.datetime(2014, 11, 22, 10, 10, 10)
            )
            date = datetime.datetime.strptime('2014-12-16 20:21:42',
                                              '%Y-%m-%d %H:%M:%S')

            self.assertEqual(
                feedback,
                [
                    {
                        'apid': '80242a4c-d870-4fce-b0c3-724c865cfbfe',
                        'alias': None,
                        'marked_inactive_on': date,
                        'gcm_registration_id': 'null'
                    }
                ]
            )
            mock_request.assert_called_with(
                method='GET',
                body='',
                url='https://go.urbanairship.com/api/apids/feedback/',
                version=3,
                params={'since': '2014-11-22T10:10:10'}
            )

    def test_device_pin_info(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'device_pin': '12345678',
                    'active': 'true',
                    'alias': 'your_user_id',
                    'tags': [
                        'tag1',
                        'tag2'
                    ],
                    'created': '2013-03-11 17:49:36',
                    'last_registration': '2014-05-01 18:00:27'
                }
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            device_pin = '12345678'
            device_info = ua.DevicePINInfo.pin_lookup(airship, device_pin)

            date_created = datetime.datetime.strptime(
                '2013-03-11 17:49:36',
                '%Y-%m-%d %H:%M:%S'
            )
            last_registration_date = datetime.datetime.strptime(
                '2014-05-01 18:00:27',
                '%Y-%m-%d %H:%M:%S'
            )

            self.assertEqual(device_info['device_pin'], '12345678')
            self.assertEqual(device_info['active'], 'true')
            self.assertEqual(device_info['alias'], 'your_user_id')
            self.assertEqual(device_info['tags'], ['tag1', 'tag2'])
            self.assertEqual(device_info['created'], date_created)
            self.assertEqual(
                device_info['last_registration'], last_registration_date
            )
