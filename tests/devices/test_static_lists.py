import unittest
import json

import mock
import requests
import csv

import urbanairship as ua


class TestStaticList(unittest.TestCase):
    def setUp(self):
        airship = ua.Airship('key', 'secret')
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
        data = ['alias,stevenh'.split(','), 'alias,marianb'.split(','), 'named_user,billg'.split(',')]
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
            results = self.device.update('this is a description', {'key': 'value'})
            self.assertEqual(results, {'ok': True})
