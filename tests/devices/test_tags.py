import unittest
import mock
import requests
import json
import urbanairship as ua


class TestTagList(unittest.TestCase):
    def test_list_tag(self):
        airship = ua.Airship('key', 'secret')
        test_list = ua.TagList(airship)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'tags': [
                        'tag1',
                        'some_tag',
                        'portland_or'
                    ]
                }
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            results = test_list.list_tags()

            self.assertEqual(
                results,
                {
                    'tags': [
                        'tag1',
                        'some_tag',
                        'portland_or'
                    ]
                }
            )


class TestTags(unittest.TestCase):
    def test_add_device(self):
        airship = ua.Airship('key', 'secret')
        test_tag = ua.Tag(airship, 'high roller')

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response.status_code = 200
            mock_request.return_value = response

            test_tag.add(
                ios_channels=[
                    '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                    '9c36e8c7-5a73-47c0-9716-99fd3d4197d8'
                ],
                android_channels=[
                    '9c36e8c7-5a73-47c0-9716-99fd3d4197d6'
                ]
            )
            self.assertEqual(
                test_tag.data,
                {
                    'ios_channels': {
                        'add': [
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d8'
                        ]
                    },
                    'android_channels': {
                        'add': [
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d6'
                        ]
                    }
                }
            )

    def test_remove_device(self):
        airship = ua.Airship('key', 'secret')
        tag = ua.Tag(airship, 'high roller')

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response.status_code = 200
            mock_request.return_value = response

            tag.remove(
                ios_channels=[
                    '9c36e8c7-5a73-47c0-9716-99fd3d4197d11'
                ],
                android_channels=[
                    '9c36e8c7-5a73-47c0-9716-99fd3d4197d12',
                    '9c36e8c7-5a73-47c0-9716-99fd3d4197d15'
                ]
            )

            self.assertEqual(
                tag.data,
                {
                    'ios_channels': {
                        'remove': [
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d11'
                        ]
                    },
                    'android_channels': {
                        'remove': [
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d12',
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d15'
                        ]
                    }
                }
            )


class TestDeleteTag(unittest.TestCase):
    def test_delete_tag(self):
        airship = ua.Airship('key', 'secret')
        test_delete = ua.DeleteTag(airship, 'high_roller')

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response.status_code = 204
            mock_request.return_value = response

            url = 'https://go.urbanairship.com/api/tags/high_roller'
            test_delete.url = url
            results = test_delete.send_delete()
            self.assertEqual(results, response)


class TestBatchTag(unittest.TestCase):
    def test_add_ios_channel(self):
        airship = ua.Airship('key', 'secret')
        batch = ua.BatchTag(airship)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                [
                    {
                        'ios_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                        'tags': [
                            'ios_test_batch_tag',
                            'tag2'
                        ]
                    }
                ]
            ).encode('utf-8')
            response.status_code = 202
            mock_request.return_value = response

            batch.add_ios_channel(
                '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                [
                    'ios_test_batch_tag',
                    'tag2'
                ]
            )

            self.assertEqual(
                batch.changelist,
                [
                    {
                        'ios_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                        'tags': [
                            'ios_test_batch_tag',
                            'tag2'
                        ]
                    }
                ]
            )

    def test_add_android_channel(self):
        airship = ua.Airship('key', 'secret')
        batch = ua.BatchTag(airship)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                [
                    {
                        'android_channel':
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                        'tags': [
                            'android_test_batch_tag',
                            'tag4'
                        ]
                    }
                ]
            ).encode('utf-8')
            response.status_code = 202
            mock_request.return_value = response

            batch.add_android_channel(
                '9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                [
                    'android_test_batch_tag',
                    'tag4'
                ]
            )

            self.assertEqual(
                batch.changelist,
                [
                    {
                        'android_channel':
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                        'tags': [
                            'android_test_batch_tag',
                            'tag4'
                        ]
                    }
                ]
            )

    def test_add_amazon_channel(self):
        airship = ua.Airship('key', 'secret')
        batch = ua.BatchTag(airship)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                [
                    {
                        'amazon_channel':
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d7',
                        'tags': [
                            'amazon_test_batch_tag',
                            'tag_6'
                        ]
                    }
                ])
            response.status_code = 202
            mock_request.return_value = response

            batch.add_amazon_channel(
                '9c36e8c7-5a73-47c0-9716-99fd3d4197d7',
                [
                    'amazon_test_batch_tag',
                    'tag_6'
                ]
            )

            self.assertEqual(batch.changelist, [
                {
                    'amazon_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d7',
                    'tags': [
                        'amazon_test_batch_tag',
                        'tag_6'
                    ]
                }
            ])

    def test_send_request(self):
        airship = ua.Airship('key', 'secret')
        batch = ua.BatchTag(airship)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                [
                    {
                        'ios_channels':
                            '0492662a-1b52-4343-a1f9-c6b0c72931c0',
                        'tags': [
                            'some_tag',
                            'some_other_tag'
                        ]
                    },
                    {
                        'android_channels':
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                        'tags': [
                            'tag_to_apply_1',
                            'tag_to_apply_2'
                        ]
                    },
                    {
                        'amazon_channels':
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d7',
                        'tags': [
                            'tag_to_apply_1',
                            'tag_to_apply_7'
                        ]
                    }
                ]).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            batch.add_ios_channel(
                '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                [
                    'apply_tag',
                    'apply_tag_2'
                ]
            )
            batch.add_android_channel(
                '9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                [
                    'apply_tag_3',
                    'apply_tag_4'
                ]
            )
            batch.send_request()

            self.assertEqual(
                batch.changelist,
                [
                    {
                        'ios_channel':
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                        'tags': [
                            'apply_tag',
                            'apply_tag_2'
                        ]
                    },
                    {
                        'android_channel':
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                        'tags': [
                            'apply_tag_3',
                            'apply_tag_4'
                        ]
                    },
                ]
            )


class TestChannelTags(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship('key', 'secret')
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
        result = self.channel_tags.send_request()

        self.assertEqual(
            result,
            [
                {
                    'ok': True,
                }
            ]
        )

    def test_android_audience(self):
        self.channel_tags.set_audience(android='android_audience')
        self.channel_tags.add('group_name', 'tag1')
        result = self.channel_tags.send_request()

        self.assertEqual(
            result,
            [
                {
                    'ok': True,
                }
            ]
        )

    def test_amazon_audience(self):
        self.channel_tags.set_audience(amazon='android_audience')
        self.channel_tags.add('group_name', 'tag1')
        result = self.channel_tags.send_request()

        self.assertEqual(
            result,
            [
                {
                    'ok': True,
                }
            ]
        )

    def test_all_audiences(self):
        self.channel_tags.set_audience('ios_audience', 'android_audience', 'amazon_audience')
        self.channel_tags.add('group_name', 'tag1')
        result = self.channel_tags.send_request()

        self.assertEqual(
            result,
            [
                {
                    'ok': True,
                }
            ]
        )

    def test_add_and_remove(self):
        self.channel_tags.set_audience('ios_audience', 'android_audience', 'amazon_audience')
        self.channel_tags.add('group_name', 'tag1')
        self.channel_tags.remove('group2_name', 'tag2')
        result = self.channel_tags.send_request()

        self.assertEqual(
            result,
            [
                {
                    'ok': True,
                }
            ]
        )

    def test_add_and_remove_and_set(self):
        self.channel_tags.set_audience('ios_audience', 'android_audience', 'amazon_audience')
        self.channel_tags.add('group_name', 'tag1')
        self.channel_tags.remove('group2_name', 'tag2')
        self.channel_tags.set('group3_name', 'tag3')

        self.assertRaises(
            ValueError,
            callableObj=self.channel_tags.send_request,
        )

    def test_remove_and_set(self):
        self.channel_tags.set_audience('ios_audience', 'android_audience', 'amazon_audience')
        self.channel_tags.remove('group2_name', 'tag2')
        self.channel_tags.set('group3_name', 'tag3')

        self.assertRaises(
            ValueError,
            callableObj=self.channel_tags.send_request,
        )

    def test_set(self):
        self.channel_tags.set_audience('ios_audience', 'android_audience', 'amazon_audience')
        self.channel_tags.set('group3_name', 'tag3')
        result = self.channel_tags.send_request()

        self.assertEqual(
            result,
            [
                {
                    'ok': True,
                }
            ]
        )

    def test_tag_lists(self):
        self.channel_tags.set_audience('ios_audience', 'android_audience', 'amazon_audience')
        self.channel_tags.set('group3_name', ['tag1', 'tag2', 'tag3'])
        result = self.channel_tags.send_request()

        self.assertEqual(
            result,
            [
                {
                    'ok': True,
                }
            ]
        )
