import unittest
import mock
import json

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestAutomation(unittest.TestCase):
    def test_create_with_single_pipeline(self):
        operation_id = "86ad9239-373d-d0a5-d5d8-04fed18f79bc"

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "ok": True,
                    "operation_id": operation_id,
                    "pipeline_urls": [
                        "https://go.urbanairship/api/pipelines/" + operation_id
                    ],
                }
            )
            response._status_code = 201
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)

            automation = ua.Automation(airship)
            pipeline = ua.Pipeline()

            pipeline.enabled = True
            pipeline.outcome = [
                {
                    "push": {
                        "audience": "triggered",
                        "notification": {"alert": "a witty test notification"},
                        "options": {"expiry": "2017-04-01T12:00:00"},
                    }
                },
                {
                    "push": {
                        "audience": "triggered",
                        "notification": {"alert": "a wittier test notification"},
                        "options": {"expiry": "2017-04-01T12:00:00"},
                    }
                },
            ]
            pipeline.name = "test_automation"
            pipeline.immediate_trigger = [
                {"tag_added": "tag_youre_it"},
                {"tag_removed": "tag_im_it"},
            ]
            pipeline.cancellation_trigger = [
                "open",
                {"custom_event": {"name": "a_custom_event"}},
            ]
            pipeline.historical_trigger = {"event": "open", "equals": 0, "days": 80}
            pipeline.constraint = [
                {"rate": {"pushes": 4, "days": 5}},
                {"rate": {"pushes": 6, "days": 10}},
            ]
            pipeline.condition = [
                {
                    "or": [
                        {"tag": {"tag_name": "VIP"}},
                        {"tag": {"tag_name": "dont_push", "negated": True}},
                    ]
                },
                {
                    "and": [
                        {"tag": {"tag_name": "NVVIP"}},
                        {"tag": {"tag_name": "push", "negated": True}},
                    ]
                },
            ]
            pipeline.timing = {
                "delay": {"seconds": 15},
                "schedule": {
                    "type": "local",
                    "miss_behavior": "cancel",
                    "dayparts": [
                        {"days_of_week": ["tuesday", "thursday", "saturday"]},
                    ],
                    "allowed_times": {
                        "start": "00:00:01",
                        "end": "23:59:59",
                    },
                },
            }

            test_response = automation.create(pipeline.payload)

            self.assertEqual(
                json.loads(test_response.content)["operation_id"], operation_id
            )

    def test_create_with_multiple_pipelines(self):
        operation_id = "86ad9239-373d-d0a5-d5d8-04fed18f79dc"

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "ok": True,
                    "operation_id": operation_id,
                    "pipeline_urls": [
                        "https://go.urbanairship/api/pipelines/"
                        + "8b64ff83-7586-4012-adad-d34ebb7df8b4",
                        "https://go.urbanairship/api/pipelines/"
                        + "0ba14c4e-6997-4a39-9231-fdf2005d3e2e",
                    ],
                }
            )
            response._status_code = 201
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)

            enabled = True
            outcome = [
                {
                    "push": {
                        "audience": "triggered",
                        "notification": {"alert": "a witty test notification"},
                        "options": {"expiry": "2017-04-01T12:00:00"},
                    }
                },
                {
                    "push": {
                        "audience": "triggered",
                        "notification": {"alert": "a wittier test notification"},
                        "options": {"expiry": "2017-04-01T12:00:00"},
                    }
                },
            ]
            name = "test_automation"
            immediate_trigger = [
                {"tag_added": "tag_youre_it"},
                {"tag_removed": "tag_im_it"},
            ]
            cancellation_trigger = [
                "open",
                {"custom_event": {"name": "a_custom_event"}},
            ]
            historical_trigger = {"event": "open", "equals": 0, "days": 80}
            constraint = [
                {"rate": {"pushes": 4, "days": 5}},
                {"rate": {"pushes": 6, "days": 10}},
            ]
            condition = [
                {
                    "or": [
                        {"tag": {"tag_name": "VIP"}},
                        {"tag": {"tag_name": "dont_push", "negated": True}},
                    ]
                },
                {
                    "and": [
                        {"tag": {"tag_name": "NVVIP"}},
                        {"tag": {"tag_name": "push", "negated": True}},
                    ]
                },
            ]
            timing = {
                "delay": {"seconds": 15},
                "schedule": {
                    "type": "local",
                    "miss_behavior": "cancel",
                    "dayparts": [
                        {"days_of_week": ["tuesday", "thursday", "saturday"]},
                    ],
                    "allowed_times": {
                        "start": "00:00:01",
                        "end": "23:59:59",
                    },
                },
            }

            pipeline1 = ua.Pipeline(
                enabled=enabled,
                outcome=outcome,
                name=name,
                immediate_trigger=immediate_trigger,
                cancellation_trigger=cancellation_trigger,
                historical_trigger=historical_trigger,
                constraint=constraint,
                condition=condition,
                timing=timing,
            )

            pipeline2 = ua.Pipeline(
                enabled=enabled,
                outcome=outcome,
                name=name,
                immediate_trigger=immediate_trigger,
                cancellation_trigger=cancellation_trigger,
                historical_trigger=historical_trigger,
                constraint=constraint,
                condition=condition,
                timing=timing,
            )

            automation = ua.Automation(airship)
            test_response = automation.create([pipeline1.payload, pipeline2.payload])

            self.assertEqual(
                json.loads(test_response.content)["pipeline_urls"],
                [
                    "https://go.urbanairship/api/pipelines/"
                    + "8b64ff83-7586-4012-adad-d34ebb7df8b4",
                    "https://go.urbanairship/api/pipelines/"
                    + "0ba14c4e-6997-4a39-9231-fdf2005d3e2e",
                ],
            )

    def test_validate_automation(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps({"ok": True})
            response._status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)

            automation = ua.Automation(airship)
            pipeline = ua.Pipeline()

            pipeline.enabled = True
            pipeline.outcome = [
                {
                    "push": {
                        "audience": "triggered",
                        "notification": {"alert": "a witty test notification"},
                        "options": {"expiry": "2017-04-01T12:00:00"},
                    }
                },
                {
                    "push": {
                        "audience": "triggered",
                        "notification": {"alert": "a wittier test notification"},
                        "options": {"expiry": "2017-04-01T12:00:00"},
                    }
                },
            ]
            pipeline.name = "test_automation"
            pipeline.immediate_trigger = [
                {"tag_added": "tag_youre_it"},
                {"tag_removed": "tag_im_it"},
            ]
            pipeline.cancellation_trigger = [
                "open",
                {"custom_event": {"name": "a_custom_event"}},
            ]
            pipeline.historical_trigger = {"event": "open", "equals": 0, "days": 80}
            pipeline.constraint = [
                {"rate": {"pushes": 4, "days": 5}},
                {"rate": {"pushes": 6, "days": 10}},
            ]
            pipeline.condition = [
                {
                    "or": [
                        {"tag": {"tag_name": "VIP"}},
                        {"tag": {"tag_name": "dont_push", "negated": True}},
                    ]
                },
                {
                    "and": [
                        {"tag": {"tag_name": "NVVIP"}},
                        {"tag": {"tag_name": "push", "negated": True}},
                    ]
                },
            ]
            pipeline.timing = {
                "delay": {"seconds": 15},
                "schedule": {
                    "type": "local",
                    "miss_behavior": "cancel",
                    "dayparts": [
                        {"days_of_week": ["tuesday", "thursday", "saturday"]},
                    ],
                    "allowed_times": {
                        "start": "00:00:01",
                        "end": "23:59:59",
                    },
                },
            }

            test_response = automation.validate(pipeline.payload)

            self.assertEqual(json.loads(test_response.content)["ok"], True)
