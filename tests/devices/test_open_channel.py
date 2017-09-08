import datetime
import json
import mock
import unittest

import requests

import urbanairship as ua


class TestOpenChannel(unittest.TestCase):
    def test_create_channel(self):
        channel_id = '37b4f6e9-8e50-4400-8246-bdfcbf7ed3be'
        address = 'some_address'
        platform = 'a_platform'
        identifiers = {
            'com.example.external_id': 'df6a6b50-9843-7894-1235-12aed4489489',
            'another_example_identifier': 'some_hash'
        }

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {'channel_id': channel_id}
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            channel = ua.OpenChannel(airship)
            channel.address = address
            channel.open_platform = platform
            channel.opt_in = True
            channel.identifiers = identifiers

            channel.create()

            self.assertEqual(channel.channel_id, channel_id)

    def test_create_channel_with_tags(self):
        channel_id = '37b4f6e9-8e50-4400-8246-bdfcbf7ed3be'
        address = 'some_address'
        platform = 'a_platform'

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {'channel_id': channel_id}
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            channel = ua.OpenChannel(airship)
            channel.address = address
            channel.open_platform = platform
            channel.opt_in = True
            channel.tags = ['a_tag']

            channel.create(set_tags=True)

            self.assertEqual(channel.channel_id, channel_id)

    def test_create_channel_requires_platform(self):
        address = 'some_address'

        airship = ua.Airship('key', 'secret')
        channel = ua.OpenChannel(airship)
        # Do not set platform
        channel.address = address
        channel.opt_in = True

        self.assertRaises(ValueError, channel.create)

    def test_create_channel_requires_address(self):
        platform = 'a_platform'

        airship = ua.Airship('key', 'secret')
        channel = ua.OpenChannel(airship)
        # Do not set address
        channel.open_platform = platform
        channel.opt_in = True

        self.assertRaises(ValueError, channel.create)

    def test_create_channel_requires_opt_in(self):
        address = 'some_address'
        platform = 'a_platform'

        airship = ua.Airship('key', 'secret')
        channel = ua.OpenChannel(airship)
        # Do not set opt in
        channel.address = address
        channel.open_platform = platform

        self.assertRaises(ValueError, channel.create)

    def test_create_channel_requires_set_tag_if_tags(self):
        address = 'some_address'
        platform = 'a_platform'

        airship = ua.Airship('key', 'secret')
        channel = ua.OpenChannel(airship)
        channel.address = address
        channel.open_platform = platform
        channel.opt_in = True

        channel.tags = ['some_tags', 'another_one']

        self.assertRaises(ValueError, channel.create)

    def test_open_channel_lookup(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "ok": "true",
                    "channel": {
                        "channel_id": "b8f9b663-0a3b-cf45-587a-be880946e881",
                        "device_type": "open",
                        "installed": "true",
                        "named_user_id": "john_doe_123",
                        "tags": ["tag_a", "tag_b"],
                        "tag_groups": {
                            "timezone": ["America/Los_Angeles"],
                            "locale_country": ["US"],
                            "locale_language": ["en"],
                            "tag_group_1": ["tag1", "tag2"],
                            "tag_group_2": ["tag1", "tag2"]
                        },
                        "created": "2017-08-08T20:41:06",
                        "address": "example@example.com",
                        "opt_in": "true",
                        "open": {
                            "open_platform_name": "email",
                            "identifiers": {
                                "com.example.external_id":
                                    "df6a6b50-9843-7894-1235-12aed4489489",
                                "another_example_identifier": "some_hash"
                            }
                        },
                        "last_registration": "2017-09-01T18:00:27"
                    }
                }
            ).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            channel_id = 'b8f9b663-0a3b-cf45-587a-be880946e881'
            open_channel_lookup = ua.OpenChannel(airship).lookup(channel_id)

            date_created = (
                datetime.datetime.strptime(
                    '2017-08-08T20:41:06',
                    '%Y-%m-%dT%H:%M:%S'
                )
            )
            date_last_registration = (
                datetime.datetime.strptime(
                    '2017-09-01T18:00:27',
                    '%Y-%m-%dT%H:%M:%S'
                )
            )

            self.assertEqual(open_channel_lookup.channel_id, channel_id)
            self.assertEqual(open_channel_lookup.device_type, 'open')
            self.assertEqual(open_channel_lookup.installed, 'true')
            self.assertEqual(open_channel_lookup.opt_in, 'true')
            self.assertEqual(open_channel_lookup.named_user_id, 'john_doe_123')
            self.assertEqual(open_channel_lookup.created, date_created)
            self.assertEqual(open_channel_lookup.open_platform, 'email')
            self.assertEqual(
                open_channel_lookup.last_registration, date_last_registration
            )
            self.assertEqual(
                open_channel_lookup.address, 'example@example.com'
            )
            self.assertListEqual(open_channel_lookup.tags, ['tag_a', 'tag_b'])
            self.assertDictEqual(
                open_channel_lookup.identifiers,
                {
                    'com.example.external_id':
                        'df6a6b50-9843-7894-1235-12aed4489489',
                    'another_example_identifier': 'some_hash'
                }
            )

    def test_open_channel_update(self):
        channel_id = 'b8f9b663-0a3b-cf45-587a-be880946e881'

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {'ok': True, 'channel_id': channel_id}
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            channel_to_update = ua.OpenChannel(airship)
            channel_to_update.channel_id = channel_id
            channel_to_update.open_platform = 'email'
            channel_to_update.tags = ['a_new_tag']
            channel_to_update.opt_in = True
            channel_to_update.address = 'example@example.com'
            channel_to_update.update(set_tags=True)

            self.assertEqual(channel_to_update.channel_id, channel_id)
