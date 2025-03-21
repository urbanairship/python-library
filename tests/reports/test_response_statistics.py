import json
import unittest
from datetime import datetime

import requests
from mock import Mock

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestResponseStats(unittest.TestCase):
    def test_response_stats(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                "push_uuid": "f133a7c8-d750-11e1-a6cf-e06995b6c872",
                "direct_responses": 45,
                "sends": 123,
                "push_type": "UNICAST_PUSH",
                "push_time": "2012-07-31 12:34:56",
            }
        ).encode("utf-8")

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        statistics = ua.reports.IndividualResponseStats(airship).get("push_id")

        self.assertEqual(statistics.push_uuid, "f133a7c8-d750-11e1-a6cf-e06995b6c872")
        self.assertEqual(statistics.direct_responses, 45)
        self.assertEqual(statistics.sends, 123)
        self.assertEqual(statistics.push_type, "UNICAST_PUSH")
        self.assertEqual(statistics.push_time, datetime(2012, 7, 31, 12, 34, 56))


class TestResponseList(unittest.TestCase):
    def setUp(self):
        self.uuid1 = "ae46a0b4-8130-4fcd-8464-0c601d0390be"
        self.uuid2 = "de4e1149-9dfb-4c29-a639-090b29bada45"
        self.uuid3 = "e91fd480-0aa1-4f70-981d-7be765d465d1"

    def test_response_list(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                "pushes": [
                    {
                        "push_uuid": self.uuid1,
                        "sends": 0,
                        "push_time": "2015-06-13 23:27:46",
                        "push_type": "UNICAST_PUSH",
                        "direct_responses": 10,
                        "group_id": self.uuid2,
                    },
                    {
                        "push_uuid": self.uuid2,
                        "sends": 1,
                        "push_time": "2015-06-29 23:42:39",
                        "push_type": "UNICAST_PUSH",
                        "direct_responses": 23,
                        "group_id": self.uuid2,
                    },
                    {
                        "push_uuid": self.uuid3,
                        "sends": 2,
                        "push_time": "2015-06-23 18:12:44",
                        "push_type": "UNICAST_PUSH",
                        "direct_responses": 7,
                    },
                ]
            }
        ).encode("utf-8")

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        start_date = datetime(2015, 6, 29)
        end_date = datetime(2015, 6, 30)
        return_list = ua.reports.ResponseList(airship, start_date, end_date)

        push_responses = []

        for response in return_list:
            push_responses.append(response)

        self.assertEqual(push_responses[0].push_uuid, self.uuid1)
        self.assertEqual(push_responses[0].sends, 0)
        self.assertEqual(push_responses[0].push_time, datetime(2015, 6, 13, 23, 27, 46))
        self.assertEqual(push_responses[0].push_type, "UNICAST_PUSH")
        self.assertEqual(push_responses[0].direct_responses, 10)
        self.assertEqual(push_responses[0].group_id, self.uuid2)

        self.assertEqual(push_responses[1].push_uuid, self.uuid2)
        self.assertEqual(push_responses[1].sends, 1)
        self.assertEqual(push_responses[1].push_time, datetime(2015, 6, 29, 23, 42, 39))
        self.assertEqual(push_responses[1].push_type, "UNICAST_PUSH")
        self.assertEqual(push_responses[1].direct_responses, 23)
        self.assertEqual(push_responses[1].group_id, self.uuid2)

        self.assertEqual(push_responses[2].push_uuid, self.uuid3)
        self.assertEqual(push_responses[2].sends, 2)
        self.assertEqual(push_responses[2].push_time, datetime(2015, 6, 23, 18, 12, 44))
        self.assertEqual(push_responses[2].push_type, "UNICAST_PUSH")
        self.assertEqual(push_responses[2].direct_responses, 7)

    def test_next_page(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                "pushes": [
                    {
                        "push_uuid": self.uuid1,
                        "sends": 0,
                        "push_time": "2015-06-13 23:27:46",
                        "push_type": "UNICAST_PUSH",
                        "direct_responses": 10,
                        "group_id": self.uuid2,
                    }
                ],
                "next_page": "next_page_url",
            }
        ).encode("utf-8")

        mock_next_response = requests.Response()
        mock_next_response._content = json.dumps(
            {
                "pushes": [
                    {
                        "push_uuid": self.uuid2,
                        "sends": 1,
                        "push_time": "2015-06-29 23:42:39",
                        "push_type": "UNICAST_PUSH",
                        "direct_responses": 23,
                        "group_id": self.uuid2,
                    }
                ]
            }
        ).encode("utf-8")

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response, mock_next_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        start_date = datetime(2015, 6, 29)
        end_date = datetime(2015, 6, 30)
        return_list = ua.reports.ResponseList(airship, start_date, end_date)

        push_responses = []

        for response in return_list:
            push_responses.append(response)

        self.assertEqual(push_responses[0].push_uuid, self.uuid1)
        self.assertEqual(push_responses[0].sends, 0)
        self.assertEqual(push_responses[0].push_time, datetime(2015, 6, 13, 23, 27, 46))
        self.assertEqual(push_responses[0].push_type, "UNICAST_PUSH")
        self.assertEqual(push_responses[0].direct_responses, 10)
        self.assertEqual(push_responses[0].group_id, self.uuid2)

        self.assertEqual(push_responses[1].push_uuid, self.uuid2)
        self.assertEqual(push_responses[1].sends, 1)
        self.assertEqual(push_responses[1].push_time, datetime(2015, 6, 29, 23, 42, 39))
        self.assertEqual(push_responses[1].push_type, "UNICAST_PUSH")
        self.assertEqual(push_responses[1].direct_responses, 23)
        self.assertEqual(push_responses[1].group_id, self.uuid2)

    def test_invalid_datetime(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        end_date = datetime(2015, 7, 2)
        self.assertRaises(
            TypeError,
            ua.reports.ResponseList,
            airship=airship,
            start_date="2015-07-01",
            end_date=end_date,
        )

    def test_empty_date(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        end_date = datetime(2015, 7, 2)
        self.assertRaises(
            TypeError,
            ua.reports.ResponseList,
            airship=airship,
            start_date=None,
            end_date=end_date,
        )


class TestDevicesReport(unittest.TestCase):
    def test_devices_report(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                "total_unique_devices": 150,
                "date_computed": "2014-10-01T08:31:54.000Z",
                "date_closed": "2014-10-01T00:00:00.000Z",
                "counts": {
                    "android": {
                        "unique_devices": 50,
                        "opted_in": 0,
                        "opted_out": 0,
                        "uninstalled": 10,
                    },
                    "ios": {
                        "unique_devices": 50,
                        "opted_in": 0,
                        "opted_out": 0,
                        "uninstalled": 10,
                    },
                },
            }
        ).encode("utf-8")

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        push_date = datetime(2014, 10, 1)
        d = ua.reports.DevicesReport(airship)
        devices = d.get(push_date)

        self.assertEqual(devices["total_unique_devices"], 150)
        self.assertEqual(devices["date_computed"], "2014-10-01T08:31:54.000Z")
        self.assertEqual(devices["date_closed"], "2014-10-01T00:00:00.000Z")
        self.assertEqual(devices["counts"]["android"]["unique_devices"], 50)
        self.assertEqual(devices["counts"]["android"]["opted_in"], 0)
        self.assertEqual(devices["counts"]["android"]["opted_out"], 0)
        self.assertEqual(devices["counts"]["android"]["uninstalled"], 10)
        self.assertEqual(devices["counts"]["ios"]["unique_devices"], 50)
        self.assertEqual(devices["counts"]["ios"]["opted_in"], 0)
        self.assertEqual(devices["counts"]["ios"]["opted_out"], 0)
        self.assertEqual(devices["counts"]["ios"]["uninstalled"], 10)

    def test_invalid_datetime(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        s = ua.reports.DevicesReport(airship)
        self.assertRaises(ValueError, s.get, date="2015-07-01")

    def test_empty_date(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        s = ua.reports.DevicesReport(airship)
        self.assertRaises(TypeError, s.get, date=None)


class TestOptInList(unittest.TestCase):
    class_to_test = ua.reports.OptInList
    response_key = "optins"

    def test_list(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                self.response_key: [
                    {"android": 50, "date": "2012-12-01 00:00:00", "ios": 23},
                    {"android": 13, "date": "2012-2-01 00:00:00", "ios": 8},
                    {"android": 5, "date": "2012-3-01 00:00:00", "ios": 88},
                ]
            }
        ).encode("utf-8")

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        start_date = datetime(2012, 12, 1)
        end_date = datetime(2012, 4, 1)
        precision = "MONTHLY"

        response_list = self.class_to_test(airship, start_date, end_date, precision)

        instantiated_list = []

        for response in response_list:
            instantiated_list.append(response)

        self.assertEqual(instantiated_list[0].android, 50)
        self.assertEqual(instantiated_list[0].date, datetime(2012, 12, 1))
        self.assertEqual(instantiated_list[0].ios, 23)

        self.assertEqual(instantiated_list[1].android, 13)
        self.assertEqual(instantiated_list[1].date, datetime(2012, 2, 1))
        self.assertEqual(instantiated_list[1].ios, 8)

        self.assertEqual(instantiated_list[2].android, 5)
        self.assertEqual(instantiated_list[2].date, datetime(2012, 3, 1))
        self.assertEqual(instantiated_list[2].ios, 88)

    def test_invalid_datetime(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        end_date = datetime(2015, 7, 2)
        self.assertRaises(
            TypeError,
            ua.reports.OptInList,
            airship=airship,
            start_date="2015-7-1",
            end_date=end_date,
            precision="HOURLY",
        )

    def test_empty_date(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        end_date = datetime(2015, 7, 2)
        self.assertRaises(
            TypeError,
            ua.reports.OptInList,
            airship=airship,
            start_date=None,
            end_date=end_date,
            precision="HOURLY",
        )

    def test_invalid_precision(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        start_date = datetime(2015, 7, 1)
        end_date = datetime(2015, 7, 2)
        self.assertRaises(
            ValueError,
            ua.reports.OptInList,
            airship=airship,
            start_date=start_date,
            end_date=end_date,
            precision="foo",
        )

    def test_empty_precision(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        start_date = datetime(2015, 7, 1)
        end_date = datetime(2015, 7, 2)
        self.assertRaises(
            TypeError,
            ua.reports.OptInList,
            airship=airship,
            start_date=start_date,
            end_date=end_date,
            precision=None,
        )


class TestOptOutList(TestOptInList):
    class_to_test = ua.reports.OptOutList
    response_key = "optouts"


class TestPushList(TestOptInList):
    class_to_test = ua.reports.PushList
    response_key = "sends"


class TestResponseReportList(TestOptInList):
    class_to_test = ua.reports.ResponseReportList
    response_key = "responses"


class TestAppOpensList(TestOptInList):
    class_to_test = ua.reports.AppOpensList
    response_key = "opens"


class TestTimeInAppList(TestOptInList):
    class_to_test = ua.reports.TimeInAppList
    response_key = "timeinapp"


class TestCustomEventsList(TestOptInList):
    class_to_test = ua.reports.CustomEventsList
    response_key = "events"


class TestWebResponseReport(TestOptInList):
    class_to_test = ua.reports.WebResponseReport
    response_key = "total_counts"
