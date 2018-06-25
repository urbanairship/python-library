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
                        'last_registration': 'None',
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
            channel_lookup = ua.ChannelInfo(airship).lookup(channel_id)

            date_created = (
                datetime.datetime.strptime(
                    '2014-04-17T23:35:15',
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
                'UNKNOWN'
            )
            self.assertEqual(
                channel_lookup.ios,
                {
                    'badge': 1,
                    'quiettime': {'start': 'null', 'end': 'null'},
                    'tz': 'null'
                }
            )
