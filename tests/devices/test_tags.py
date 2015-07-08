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
                    'audience': {
                        'ios_channel': [
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d8'
                        ],
                        'android_channel': [
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d6'
                        ]
                    },
                    'add': {
                        'device': 'high roller'
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
                    'audience': {
                        'ios_channel': [
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d11'
                        ],
                        'android_channel': [
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d12',
                            '9c36e8c7-5a73-47c0-9716-99fd3d4197d15'
                        ]
                    },
                    'remove': {
                        'device': 'high roller'
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

        batch.add_ios_channel(
            '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
            ['ios_test_batch_tag', 'tag2']
        )

        self.assertEqual(
            batch.ios_payload,
            {
                'audience': {
                    'ios_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d5'
                },
                'add': {
                    'device': ['ios_test_batch_tag', 'tag2']
                }
            }
        )

    def test_add_android_channel(self):
        airship = ua.Airship('key', 'secret')
        batch = ua.BatchTag(airship)

        batch.add_android_channel(
            '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
            ['ios_test_batch_tag', 'tag2']
        )

        self.assertEqual(
            batch.android_payload,
            {
                'audience': {
                    'android_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d5'
                },
                'add': {
                    'device': ['ios_test_batch_tag', 'tag2']
                }
            }
        )

    def test_add_amazon_channel(self):
        airship = ua.Airship('key', 'secret')
        batch = ua.BatchTag(airship)

        batch.add_amazon_channel(
            '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
            ['ios_test_batch_tag', 'tag2']
        )

        self.assertEqual(
            batch.amazon_payload,
            {
                'audience': {
                    'amazon_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d5'
                },
                'add': {
                    'device': ['ios_test_batch_tag', 'tag2']
                }
            }
        )