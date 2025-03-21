import datetime
import json
import unittest

import mock
import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.name = "Experiment Test"
        self.audience = "all"
        self.description = "just testing"
        self.device_types = ["ios", "android"]
        self.campaigns = ua.campaigns(categories=["campaign", "categories"])
        self.operation_id = "d67d4de6-934f-4ebb-aef0-250d89699b6b"
        self.experiment_id = "f0c975e4-c01a-436b-92a0-2a360f87b211"
        self.push_id = "0edb9e6f-2198-4c42-aada-5a49eb03bcbb"

        # push_1 = self.airship.create_push()
        push_1 = ua.Push(self.airship)
        push_1.notification = ua.notification(alert="test message 1")

        push_2 = ua.Push(self.airship)
        push_2.notification = ua.notification(alert="test message 2")

        push_3 = ua.Push(self.airship)
        push_3.notification = ua.notification(alert="test message 1")
        push_3.in_app = ua.in_app(
            alert="This part appears in-app!", display_type="banner"
        )

        push_4 = ua.Push
        push_4.notification = ua.notification(alert="test message 2")
        push_4.in_app = ua.in_app(
            alert="This part appears in-app!",
            display_type="banner",
            expiry="2025-10-14T12:00:00",
            display={"position": "top"},
            actions={"add_tag": "in-app"},
        )

        variant_1 = ua.Variant(
            push_1, description="A description of the variant", name="Testing"
        )
        variant_2 = ua.Variant(push_2)

        variant_3 = ua.Variant(
            push_3,
            description="A description of the variant one",
            name="Testing",
            schedule=ua.scheduled_time(datetime.datetime(2025, 10, 10, 18, 45, 30)),
            weight=2,
        )
        variant_4 = ua.Variant(
            push_4,
            description="A description of the variant two",
            name="Testing",
            schedule=ua.scheduled_time(datetime.datetime(2025, 10, 10, 18, 45, 30)),
            weight=3,
        )

        self.variants_1 = [variant_1, variant_2]
        self.variants_2 = [variant_3, variant_4]

    def test_simple_experiment(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "ok": True,
                    "operation_id": self.operation_id,
                    "experiment_id": self.experiment_id,
                    "push_id": self.push_id,
                }
            ).encode("utf-8")
            response.status_code = 201
            mock_request.return_value = response

            experiment_object = ua.Experiment(
                name=self.name,
                audience=self.audience,
                device_types=self.device_types,
                campaigns=self.campaigns,
                variants=self.variants_1,
                description=self.description,
            )
            experiment_payload = {
                "name": "Experiment Test",
                "audience": "all",
                "description": "just testing",
                "device_types": ["ios", "android"],
                "campaigns": {"categories": ["campaign", "categories"]},
                "variants": [
                    {
                        "description": "A description of the variant",
                        "name": "Testing",
                        "push": {"notification": {"alert": "test message 1"}},
                    },
                    {"push": {"notification": {"alert": "test message 2"}}},
                ],
            }
            self.assertDictEqual(experiment_object.payload, experiment_payload)

    def test_full_experiment(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "ok": True,
                    "operation_id": self.operation_id,
                    "experiment_id": self.experiment_id,
                    "push_id": self.push_id,
                }
            ).encode("utf-8")
            response.status_code = 201
            mock_request.return_value = response

            experiment_object = ua.Experiment(
                name=self.name,
                audience=self.audience,
                control=0.5,
                description=self.description,
                device_types=self.device_types,
                campaigns=self.campaigns,
                variants=self.variants_2,
            )
            experiment_payload = {
                "name": "Experiment Test",
                "audience": "all",
                "control": 0.5,
                "description": "just testing",
                "device_types": ["ios", "android"],
                "campaigns": {"categories": ["campaign", "categories"]},
                "variants": [
                    {
                        "description": "A description of the variant one",
                        "name": "Testing",
                        "schedule": {"scheduled_time": "2025-10-10T18:45:30"},
                        "weight": 2,
                        "push": {
                            "notification": {"alert": "test message 1"},
                            "in_app": {
                                "alert": "This part appears in-app!",
                                "display_type": "banner",
                            },
                        },
                    },
                    {
                        "description": "A description of the variant two",
                        "name": "Testing",
                        "schedule": {"scheduled_time": "2025-10-10T18:45:30"},
                        "weight": 3,
                        "push": {
                            "notification": {"alert": "test message 2"},
                            "in_app": {
                                "alert": "This part appears in-app!",
                                "display_type": "banner",
                                "expiry": "2025-10-14T12:00:00",
                                "display": {"position": "top"},
                                "actions": {"add_tag": "in-app"},
                            },
                        },
                    },
                ],
            }
            print(str(experiment_object.payload))
            self.assertEqual(experiment_object.payload, experiment_payload)
