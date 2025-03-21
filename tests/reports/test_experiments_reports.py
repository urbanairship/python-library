import json
import unittest

import requests
from mock import Mock

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestExperimentsReports(unittest.TestCase):
    def test_experiment_overview(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                "app_key": TEST_KEY,
                "experiment_id": "24cf2af1-9961-4f3f-b301-75505c240358",
                "push_id": "bb74f63c-c1c8-4618-800d-a04478e7d28c",
                "created": "2021-11-12 13:44:09",
                "sends": 6,
                "direct_responses": 0,
                "influenced_responses": 0,
                "web_clicks": 0,
                "web_sessions": 0,
                "variants": [
                    {
                        "id": 0,
                        "name": "Test A",
                        "audience_pct": 80.0,
                        "sends": 6,
                        "direct_responses": 0,
                        "direct_response_pct": 0.0,
                        "indirect_responses": 0,
                        "indirect_response_pct": 0.0,
                    }
                ],
                "control": {
                    "audience_pct": 20.0,
                    "sends": 1,
                    "responses": 0,
                    "response_rate_pct": 0.0,
                },
            }
        ).encode("UTF-8")

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        overview = ua.ExperimentReport(airship).get_overview(
            push_id="bb74f63c-c1c8-4618-800d-a04478e7d28c"
        )
        self.assertEqual(overview.get("app_key"), TEST_KEY)
        self.assertEqual(overview.get("sends"), 6)
        self.assertEqual(type(overview.get("variants")), list)
        self.assertEqual(type(overview.get("control")), dict)

    def test_variant_overview(self):
        mock_response = requests.Response()
        mock_response._content = json.dumps(
            {
                "app_key": TEST_KEY,
                "experiment_id": "24cf2af1-9961-4f3f-b301-75505c240358",
                "push_id": "bb74f63c-c1c8-4618-800d-a04478e7d28c",
                "created": "2021-11-12 13:44:09",
                "variant": 0,
                "variant_name": "Test A",
                "sends": 6,
                "direct_responses": 0,
                "influenced_responses": 0,
                "platforms": {
                    "amazon": {
                        "type": "devicePlatformBreakdown",
                        "direct_responses": 0,
                        "influenced_responses": 0,
                        "sends": 0,
                    },
                    "ios": {
                        "type": "devicePlatformBreakdown",
                        "direct_responses": 0,
                        "influenced_responses": 0,
                        "sends": 5,
                    },
                    "web": {
                        "type": "webPlatformBreakdown",
                        "direct_responses": 0,
                        "indirect_responses": 0,
                        "sends": 0,
                    },
                    "android": {
                        "type": "devicePlatformBreakdown",
                        "direct_responses": 0,
                        "influenced_responses": 0,
                        "sends": 1,
                    },
                },
            }
        ).encode("UTF-8")

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [mock_response]

        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        variant = ua.ExperimentReport(airship).get_variant(
            push_id="bb74f63c-c1c8-4618-800d-a04478e7d28c", variant_id=0
        )

        self.assertEqual(variant.get("app_key"), TEST_KEY)
        self.assertEqual(variant.get("variant"), 0)
