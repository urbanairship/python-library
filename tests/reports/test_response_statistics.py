import unittest
import requests
from mock import Mock
import json

import urbanairship as ua

class TestResponseStatistics(unittest.TestCase):
    def test_Response_Statistics(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps({
            "push_uuid": "f133a7c8-d750-11e1-a6cf-e06995b6c872",
            "direct_responses": "45",
            "sends": 123,
            "push_type": "UNICAST_PUSH",
            "push_time": "2012-07-31 12:34:56"
        }).encode('utf-8')

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [ mock_response ]

        airship = ua.Airship('key', 'secret')
        statistics = ua.IndividualResponseStats(airship).get('push_id')

        self.assertEqual(statistics['push_uuid'], "f133a7c8-d750-11e1-a6cf-e06995b6c872")
        self.assertEqual(statistics['direct_responses'], "45")
        self.assertEqual(statistics['sends'], 123)
        self.assertEqual(statistics['push_type'], "UNICAST_PUSH")
        self.assertEqual(statistics['push_time'], "2012-07-31 12:34:56")
