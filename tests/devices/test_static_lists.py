import unittest
import json
import mock
import csv
from datetime import datetime

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestStaticList(unittest.TestCase):
    def setUp(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.name = 'ce-testlist'
        self.device = ua.StaticList(airship, self.name)

    def test_create(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({'ok': True}).encode('utf-8')
            mock_request.return_value = response

            results = self.device.create()
            self.assertEqual(results, {'ok': True})

    def test_upload(self):
        data = [
            'alias,stevenh'.split(','),
            'alias,marianb'.split(','),
            'named_user,billg'.split(',')
        ]
        self.path = 'test_data.csv'

        with open(self.path, "wt") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({'ok': True}).encode('utf-8')
            mock_request.return_value = response
            csv_file = open(self.path, 'rb')
            results = self.device.upload(csv_file)
            csv_file.close()
            self.assertEqual(results, {'ok': True})

    def test_lookup(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            data = {
                "ok": True,
                "name": self.name,
                "description": "loyalty program platinum members",
                "extra": {"key": "value"},
                "created": "2013-08-08T20:41:06",
                "last_updated": "2014-05-01T18:00:27",
                "channel_count": 1000,
                "status": "ready"
            }
            response._content = json.dumps(data).encode('utf-8')
            mock_request.return_value = response

            results = self.device.create()
            self.assertEqual(results, data)

    def test_update(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({'ok': True}).encode('utf-8')
            mock_request.return_value = response
            self.device.description = 'this is a description'
            self.device.extra = {'key': 'value'}
            results = self.device.update()
            self.assertEqual(results, {'ok': True})

    def test_delete(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response.status_code = 204
            mock_request.return_value = response
            results = self.device.delete()
            self.assertEqual(results.status_code, 204)


class TestStaticLists(unittest.TestCase):
    def test_static_list(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                'lists': [
                    {
                        'name': 'ca-testlist',
                        'description': 'this little list',
                        'extra': {'key': 'value'},
                        'created': '2015-06-29 23:42:39',
                        'last_updated': '2015-06-30 23:42:39',
                        'channel_count': 123,
                        'status': 'ready'
                    },
                    {
                        'name': 'ca-testlist2',
                        'description': 'this little list2',
                        'extra': {'key': 'value'},
                        'created': '2015-05-29 23:42:39',
                        'last_updated': '2015-05-30 23:42:39',
                        'channel_count': 23,
                        'status': 'processing'
                    },
                    {
                        'name': 'ca-testlist3',
                        'description': 'this little list3',
                        'extra': {'key': 'value'},
                        'created': '2015-04-29 23:42:39',
                        'last_updated': '2015-04-30 23:42:39',
                        'channel_count': 1500,
                        'status': 'ready'
                    },
                ]
            }
        ).encode('utf-8')

        ua.Airship._request = mock.Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        return_list = ua.devices.StaticLists(airship)

        responses = []

        for response in return_list:
            responses.append(response)

        self.assertEqual(responses[0].name, 'ca-testlist')
        self.assertEqual(responses[0].description, 'this little list')
        self.assertEqual(responses[0].extra, {'key': 'value'})
        self.assertEqual(
            responses[0].created, datetime(2015, 6, 29, 23, 42, 39)
        )
        self.assertEqual(
            responses[0].last_updated, datetime(2015, 6, 30, 23, 42, 39)
        )
        self.assertEqual(responses[0].channel_count, 123)
        self.assertEqual(responses[0].status, 'ready')

        self.assertEqual(responses[1].name, 'ca-testlist2')
        self.assertEqual(responses[1].description, 'this little list2')
        self.assertEqual(responses[1].extra, {'key': 'value'})
        self.assertEqual(
            responses[1].created, datetime(2015, 5, 29, 23, 42, 39)
        )
        self.assertEqual(
            responses[1].last_updated, datetime(2015, 5, 30, 23, 42, 39)
             )
        self.assertEqual(responses[1].channel_count, 23)
        self.assertEqual(responses[1].status, 'processing')

        self.assertEqual(responses[2].name, 'ca-testlist3')
        self.assertEqual(responses[2].description, 'this little list3')
        self.assertEqual(responses[2].extra, {'key': 'value'})
        self.assertEqual(
            responses[2].created, datetime(2015, 4, 29, 23, 42, 39)
        )
        self.assertEqual(
            responses[2].last_updated, datetime(2015, 4, 30, 23, 42, 39)
        )
        self.assertEqual(responses[2].channel_count, 1500)
        self.assertEqual(responses[2].status, 'ready')

    def test_next_page(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                'lists': [
                    {
                        'name': 'ca-testlist',
                        'description': 'this little list',
                        'extra': {'key': 'value'},
                        'created': '2015-06-29 23:42:39',
                        'last_updated': '2015-06-30 23:42:39',
                        'channel_count': 123,
                        'status': 'ready'
                    }
                ],
                'next_page': 'next_page_url'
            }
        ).encode('utf-8')

        mock_next_response = requests.Response()
        mock_next_response._content = json.dumps(
            {
                'lists': [
                    {
                        'name': 'ca-testlist2',
                        'description': 'this little list2',
                        'extra': {'key': 'value'},
                        'created': '2015-05-29 23:42:39',
                        'last_updated': '2015-05-30 23:42:39',
                        'channel_count': 23,
                        'status': 'processing'
                    },
                ]
            }
        ).encode('utf-8')

        ua.Airship._request = mock.Mock()
        ua.Airship._request.side_effect = [mock_response, mock_next_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        return_list = ua.devices.StaticLists(airship)

        responses = []

        for response in return_list:
            responses.append(response)

        self.assertEqual(responses[0].name, 'ca-testlist')
        self.assertEqual(responses[0].description, 'this little list')
        self.assertEqual(responses[0].extra, {'key': 'value'})
        self.assertEqual(
            responses[0].created, datetime(2015, 6, 29, 23, 42, 39)
        )
        self.assertEqual(
            responses[0].last_updated, datetime(2015, 6, 30, 23, 42, 39)
        )
        self.assertEqual(responses[0].channel_count, 123)
        self.assertEqual(responses[0].status, 'ready')

        self.assertEqual(responses[1].name, 'ca-testlist2')
        self.assertEqual(responses[1].description, 'this little list2')
        self.assertEqual(responses[1].extra, {'key': 'value'})
        self.assertEqual(
            responses[1].created, datetime(2015, 5, 29, 23, 42, 39)
        )
        self.assertEqual(
            responses[1].last_updated, datetime(2015, 5, 30, 23, 42, 39)
        )
        self.assertEqual(responses[1].channel_count, 23)
        self.assertEqual(responses[1].status, 'processing')
