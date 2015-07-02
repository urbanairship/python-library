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


class TestDevicesReportAPI(unittest.TestCase):
    def test_devices_report(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps({
            "total_unique_devices": 150,
            "date_computed": "2014-10-01T08:31:54.000Z",
            "date_closed": "2014-10-01T00:00:00.000Z",
            "counts": {
                "android": {
                    "unique_devices": 50,
                    "opted_in": 0,
                    "opted_out": 0,
                    "uninstalled": 10
                },
                "ios": {
                    "unique_devices": 50,
                    "opted_in": 0,
                    "opted_out": 0,
                    "uninstalled": 10
                },
            }
        }).encode('utf-8')

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship('key', 'secret')
        push_date = datetime(2014, 10, 1)
        d = ua.reports.DevicesReportAPI(airship)
        devices = d.get(push_date)

        self.assertEqual(devices['total_unique_devices'], 150)
        self.assertEqual(devices['date_computed'], "2014-10-01T08:31:54.000Z")
        self.assertEqual(devices['date_closed'], "2014-10-01T00:00:00.000Z")
        self.assertEqual(devices['counts']['android']['unique_devices'], 50)
        self.assertEqual(devices['counts']['android']['opted_in'], 0)
        self.assertEqual(devices['counts']['android']['opted_out'], 0)
        self.assertEqual(devices['counts']['android']['uninstalled'], 10)
        self.assertEqual(devices['counts']['ios']['unique_devices'], 50)
        self.assertEqual(devices['counts']['ios']['opted_in'], 0)
        self.assertEqual(devices['counts']['ios']['opted_out'], 0)
        self.assertEqual(devices['counts']['ios']['uninstalled'], 10)
