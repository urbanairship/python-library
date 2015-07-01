import unittest
import requests
from mock import Mock
import json
from datetime import datetime
import urbanairship as ua


class TestResponseStats(unittest.TestCase):
    def test_response_stats(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps({
            "push_uuid": "f133a7c8-d750-11e1-a6cf-e06995b6c872",
            "direct_responses": 45,
            "sends": 123,
            "push_type": "UNICAST_PUSH",
            "push_time": "2012-07-31 12:34:56"
        }).encode('utf-8')

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship('key', 'secret')
        statistics = ua.reports.IndividualResponseStats(airship).get('push_id')

        self.assertEqual(statistics['push_uuid'], "f133a7c8-d750-11e1-a6cf-e06995b6c872")
        self.assertEqual(statistics['direct_responses'], 45)
        self.assertEqual(statistics['sends'], 123)
        self.assertEqual(statistics['push_type'], "UNICAST_PUSH")
        self.assertEqual(statistics['push_time'], "2012-07-31 12:34:56")


class TestResponseListing(unittest.TestCase):
    def test_response_listing(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps({
            "next_page": "next_url",
            "pushes": [
                {
                    "push_uuid": "f133a7c8-d750-11e1-a6cf-e06995b6c872",
                    "push_time": "2016-06-30 12:34:56",
                    "push_type": "UNICAST_PUSH",
                    "direct_responses": 10,
                    "sends": "123",
                    "group_id": "04911800-f48d-11e2-acc5-90e2bf027020"
                }
            ]
        }).encode('utf-8')

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship('key', 'secret')
        start_date = datetime(2015, 6, 29)
        end_date = datetime(2015, 6, 30)
        listing = ua.reports.ResponseListing(airship).get(start_date, end_date, None, None)
        self.assertEqual(listing['next_page'], "next_url")
        self.assertEqual(listing['pushes'][0]['push_uuid'], "f133a7c8-d750-11e1-a6cf-e06995b6c872")
        self.assertEqual(listing['pushes'][0]['push_time'], "2016-06-30 12:34:56")
        self.assertEqual(listing['pushes'][0]['push_type'], "UNICAST_PUSH")
        self.assertEqual(listing['pushes'][0]['direct_responses'], 10)
        self.assertEqual(listing['pushes'][0]['sends'], "123")
        self.assertEqual(listing['pushes'][0]['group_id'], "04911800-f48d-11e2-acc5-90e2bf027020")

    def test_invalid_datetime(self):
        airship = ua.Airship('key', 'secret')
        s = ua.reports.ResponseListing(airship)
        end_date = datetime(2015, 7, 2)
        self.assertRaises(
            ValueError,
            callableObj=s.get,
            start_date='2015-07-01',
            end_date=end_date
        )

    def test_empty_date(self):
        airship = ua.Airship('key', 'secret')
        s = ua.reports.ResponseListing(airship)
        end_date = datetime(2015, 7, 2)
        self.assertRaises(
            TypeError,
            callableObj=s.get,
            start_date=None,
            end_date=end_date
        )
