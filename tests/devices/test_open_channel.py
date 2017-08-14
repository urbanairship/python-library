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

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {'channel_id': channel_id}
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            channel = ua.OpenChannel()
            channel.address = address
            channel.open_platform = platform
            channel.opt_in = True

            channel.create(airship, hydrate=False)

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
            channel = ua.OpenChannel()
            channel.address = address
            channel.open_platform = platform
            channel.opt_in = True
            channel.tags = ['a_tag']

            channel.create(airship, set_tags=True, hydrate=False)

            self.assertEqual(channel.channel_id, channel_id)

    def test_create_channel_requires_platform(self):
        address = 'some_address'

        airship = ua.Airship('key', 'secret')
        channel = ua.OpenChannel()
        # Do not set platform
        channel.address = address
        channel.opt_in = True

        with self.assertRaises(ValueError):
            channel.create(airship)

    def test_create_channel_requires_address(self):
        platform = 'a_platform'

        airship = ua.Airship('key', 'secret')
        channel = ua.OpenChannel()
        # Do not set address
        channel.open_platform = platform
        channel.opt_in = True

        with self.assertRaises(ValueError):
            channel.create(airship)

    def test_create_channel_requires_opt_in(self):
        address = 'some_address'
        platform = 'a_platform'

        airship = ua.Airship('key', 'secret')
        channel = ua.OpenChannel()
        # Do not set opt in
        channel.address = address
        channel.open_platform = platform

        with self.assertRaises(ValueError):
            channel.create(airship)

    def test_create_channel_requires_set_tag_if_tags(self):
        address = 'some_address'
        platform = 'a_platform'

        airship = ua.Airship('key', 'secret')
        channel = ua.OpenChannel()
        channel.address = address
        channel.open_platform = platform
        channel.opt_in = True

        channel.tags = ['some_tags', 'another_one']

        with self.assertRaises(ValueError):
            channel.create(airship)
