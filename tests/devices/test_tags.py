import unittest
import mock
import json

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestChannelTags(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.channel_tags = ua.ChannelTags(self.airship)
        self.mock_response = requests.Response()
        self.mock_response._content = json.dumps(
            [
                {
                    'ok': True,
                }
            ]).encode('utf-8')

        ua.Airship._request = mock.Mock()
        ua.Airship._request.side_effect = [self.mock_response]

    def test_ios_audience(self):
        self.channel_tags.set_audience('ios_audience')
        self.channel_tags.add('group_name', 'tag1')
        result = self.channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_android_audience(self):
        self.channel_tags.set_audience(android='android_audience')
        self.channel_tags.add('group_name', 'tag1')
        result = self.channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_amazon_audience(self):
        self.channel_tags.set_audience(amazon='android_audience')
        self.channel_tags.add('group_name', 'tag1')
        result = self.channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_web_audience(self):
        self.channel_tags.set_audience(web='web_audience')
        self.channel_tags.add('group_name', 'tag4')
        result = self.channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_all_audiences(self):
        self.channel_tags.set_audience('ios_audience',
                                       'android_audience',
                                       'amazon_audience',
                                       'web_audience'
                                       )
        self.channel_tags.add('group_name', 'tag1')
        result = self.channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_add_and_remove(self):
        self.channel_tags.set_audience(
            'ios_audience',
            'android_audience',
            'amazon_audience',
            'web_audience'
        )
        self.channel_tags.add('group_name', 'tag1')
        self.channel_tags.remove('group2_name', 'tag2')
        result = self.channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_add_and_remove_and_set(self):
        self.channel_tags.set_audience(
            'ios_audience',
            'android_audience',
            'amazon_audience'
        )
        self.channel_tags.add('group_name', 'tag1')
        self.channel_tags.remove('group2_name', 'tag2')
        self.channel_tags.set('group3_name', 'tag3')

        self.assertRaises(
            ValueError,
            callableObj=self.channel_tags.send,
        )

    def test_remove_and_set(self):
        self.channel_tags.set_audience(
            'ios_audience',
            'android_audience',
            'amazon_audience'
            'web_audience'
        )
        self.channel_tags.remove('group2_name', 'tag2')
        self.channel_tags.set('group3_name', 'tag3')

        self.assertRaises(
            ValueError,
            callableObj=self.channel_tags.send,
        )

    def test_set(self):
        self.channel_tags.set_audience('ios_audience',
                                       'android_audience',
                                       'amazon_audience',
                                       'web_audience'
                                       )
        self.channel_tags.set('group3_name', 'tag3')
        result = self.channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_tag_lists(self):
        self.channel_tags.set_audience(
            'ios_audience',
            'android_audience',
            'amazon_audience'
        )
        self.channel_tags.set('group3_name', ['tag1', 'tag2', 'tag3'])
        result = self.channel_tags.send()

        self.assertEqual(result, [{'ok': True}])


class TestOpenChannelTags(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.open_channel_tags = ua.OpenChannelTags(self.airship)
        self.mock_response = requests.Response()
        self.mock_response._content = json.dumps(
            [{'ok': True}]).encode('utf-8')

        ua.Airship._request = mock.Mock()
        ua.Airship._request.side_effect = [self.mock_response]

    def test_set_audience(self):
        self.open_channel_tags.set_audience('new_email@example.com', 'email')

        self.assertEqual(
            self.open_channel_tags.audience,
            {
                'address': 'new_email@example.com',
                'open_platform_name': 'email'
            }
        )

    def test_add(self):
        self.open_channel_tags.set_audience('new_email@example.com', 'email')
        self.open_channel_tags.add('group1', ['tag1', 'tag2', 'tag3'])
        result = self.open_channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_remove(self):
        self.open_channel_tags.set_audience('new_email@example.com', 'email')
        self.open_channel_tags.remove('group1', ['tag1', 'tag2', 'tag3'])
        result = self.open_channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_set(self):
        self.open_channel_tags.set_audience('new_email@example.com', 'email')
        self.open_channel_tags.set('group1', ['tag1', 'tag2', 'tag3'])
        result = self.open_channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_add_remove(self):
        self.open_channel_tags.set_audience('new_email@example.com', 'email')
        self.open_channel_tags.add('group1', ['tag1', 'tag2', 'tag3'])
        self.open_channel_tags.remove('group2', ['tag21', 'tag22', 'tag23'])
        result = self.open_channel_tags.send()

        self.assertEqual(result, [{'ok': True}])

    def test_add_remove_set(self):
        self.open_channel_tags.set_audience('new_email@example.com', 'email')
        self.open_channel_tags.add('group1', ['tag1', 'tag2', 'tag3'])
        self.open_channel_tags.remove('group2', ['tag21', 'tag22', 'tag23'])
        self.open_channel_tags.set('group1', ['tag1', 'tag2', 'tag3'])

        with self.assertRaises(ValueError):
            self.open_channel_tags.send()

    def test_send_no_tags(self):
        self.open_channel_tags.set_audience('new_email@example.com', 'email')

        with self.assertRaises(ValueError):
            self.open_channel_tags.send()
