# import json
import unittest
import mock
import requests
import urbanairship as ua


class TestTagList(unittest.TestCase):

    def test_list_tag(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = ('''{"tags": ["tag1", "some_tag", "portland_or"]}''')
            response.status_code = 200
            mock_request.return_value = response

#            url = "https://go.urbanairship.com/api/tags/"

            airship = ua.Airship("key", "secret")
            test_list = ua.TagList(airship)
            results = test_list.listTags()
            self.assertEqual(results, {     # AssertionError, first arg
                "tags": [
                    "tag1",
                    "some_tag",
                    "portland_or"
                ]
            })


class TestTags(unittest.TestCase):

    def test_add_device(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
#            response._content = ('''{"ios_channels": {"add": ["9c36e8c7-5a73-47c0-9716-99fd3d4197d5", "9c36e8c7-5a73-47c0-9716-99fd3d4197d8"]}, "android_channels": {"add": ["9c36e8c7-5a73-47c0-9716-99fd3d4197d6"]}}''')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship("key", "secret")
            test_tag = ua.Tag(airship, "high roller")
            test_tag.add(ios_channels=['9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                                       '9c36e8c7-5a73-47c0-9716-99fd3d4197d8'],
                     android_channels=['9c36e8c7-5a73-47c0-9716-99fd3d4197d6'])
            self.assertEqual(test_tag.data, {
                "ios_channels": {
                    "add": [
                        "9c36e8c7-5a73-47c0-9716-99fd3d4197d5",
                        "9c36e8c7-5a73-47c0-9716-99fd3d4197d8"
                    ]
                },
                "android_channels": {
                    "add": [
                        "9c36e8c7-5a73-47c0-9716-99fd3d4197d6"]
                }
            })

    def test_remove_device(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
#            response._content = ('''not using this line''')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship("key", "secret")
            tag = ua.Tag(airship, "high roller")
            tag.remove(ios_channels=['9c36e8c7-5a73-47c0-9716-99fd3d4197d11'],
                     android_channels=['9c36e8c7-5a73-47c0-9716-99fd3d4197d12',
                                      '9c36e8c7-5a73-47c0-9716-99fd3d4197d15'])
#            print tag.data
            self.assertEqual(tag.data, {
                "ios_channels": {
                    "remove": [
                        "9c36e8c7-5a73-47c0-9716-99fd3d4197d11"
                    ]
                },
                "android_channels": {
                    "remove": [
                        "9c36e8c7-5a73-47c0-9716-99fd3d4197d12",
                        "9c36e8c7-5a73-47c0-9716-99fd3d4197d15"
                    ]
                }
            })


class TestDeleteTag(unittest.TestCase):

    def test_list_tag(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = ('''That was a success.''')
            response.status_code = 200
            mock_request.return_value = response

#            url = "https://go.urbanairship.com/api/tags/tag_name"

            airship = ua.Airship("key", "secret")
            test_delete = ua.DeleteTag(airship, "holiday_tag")
            results = test_delete.send_delete()
#            print test_delete
#            print results
            self.assertEqual(results, response.status_code)  #AssertionError - fix args
#            self.assertRaises(ValueError,)   # look at def test_cancel in TestPush()

class TestBatchTag(unittest.TestCase):

    def test_addIOSChannel(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = ([
            {'ios_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
             'tags': ['ios_test_batch_tag', 'tag2']}
            ])
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            batch = ua.BatchTag(airship)
            batch.addIOSChannel('9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                                ['ios_test_batch_tag', 'tag2'])

            self.assertEqual(batch.changelist, [
                {'ios_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                 'tags': ['ios_test_batch_tag', 'tag2']}
            ])

    def test_addAndroidChannel(self):
        batch = ua.BatchTag(None)
        batch.addAndroidChannel('9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                               ['android_test_batch_tag', 'tag4'])

        self.assertEqual(batch.changelist, [
            {
                'android_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                'tags': ['android_test_batch_tag', 'tag4']
            }
        ])

    def test_addAmazonChannel(self):
        batch = ua.BatchTag(None)
        batch.addAmazonChannel('9c36e8c7-5a73-47c0-9716-99fd3d4197d7',
                              ['amazon_test_batch_tag', 'tag_6']),

        self.assertEqual(batch.changelist, [
            {
                'amazon_channel': '9c36e8c7-5a73-47c0-9716-99fd3d4197d7',
                'tags': ['amazon_test_batch_tag', 'tag_6']
            }
        ])

    def test_send_request(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = (
              '''[
                    {
                      "ios_channels": "0492662a-1b52-4343-a1f9-c6b0c72931c0",
                      "tags": [
                          "some_tag",
                          "some_other_tag"
                      ]
                    },
                    {
                      "android_channels": "9c36e8c7-5a73-47c0-9716-99fd3d4197d6",
                      "tags": [
                          "tag_to_apply_1",
                          "tag_to_apply_2"
                      ]
                    },
                    {
                      "amazon_channels": "9c36e8c7-5a73-47c0-9716-99fd3d4197d7",
                      "tags": [
                           "tag_to_apply_1",
                           "tag_to_apply_7"
                      ]
                    }
                  ]''')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            batch = ua.BatchTag(airship)
            batch.addIOSChannel('9c36e8c7-5a73-47c0-9716-99fd3d4197d5',
                               ["apply_tag", "apply_tag_2"])
            batch.addAndroidChannel('9c36e8c7-5a73-47c0-9716-99fd3d4197d6',
                               ["apply_tag_3", "apply_tag_4"])
            batch.send_request()
            self.assertEqual(batch.changelist, [
                    {
                        "ios_channel": "9c36e8c7-5a73-47c0-9716-99fd3d4197d5",
                        "tags": [
                            "apply_tag",
                            "apply_tag_2"
                        ]
                    },
                    {
                        "android_channel": "9c36e8c7-5a73-47c0-9716-99fd3d4197d6",
                        "tags": [
                            "apply_tag_3",
                            "apply_tag_4"
                        ]
                    },
                ])
