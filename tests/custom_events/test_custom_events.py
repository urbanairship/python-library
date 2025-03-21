import datetime
import unittest

import urbanairship as ua
from tests import TEST_KEY, TEST_TOKEN


class TestCustomEvent(unittest.TestCase):
    def setUp(self):
        airship = ua.BearerTokenClient(key=TEST_KEY, token=TEST_TOKEN)

        self.event = ua.CustomEvent(
            airship=airship, name="test_event", user=ua.named_user("test_named_user")
        )

    def test_minimum_custom_event(self):
        self.assertEqual(
            self.event._payload,
            {
                "body": {"name": "test_event"},
                "user": {"named_user_id": "test_named_user"},
            },
        )

    def test_minimum_event_channel(self):
        self.event.user = ua.channel("0617a35e-b0c2-4b1c-9c41-586ca6b081d6")

        self.assertEqual(
            self.event._payload,
            {
                "body": {"name": "test_event"},
                "user": {"channel": "0617a35e-b0c2-4b1c-9c41-586ca6b081d6"},
            },
        )

    def test_full_custom_event(self):
        properties = {"key": "value", "nested": {"another": "pair"}}

        self.event.occurred = datetime.datetime(2022, 1, 11, 11, 30, 00)
        self.event.session_id = "0617a35e-b0c2-4b1c-9c41-586ca6b081d6"
        self.event.interaction_id = "test_interaction_id"
        self.event.interaction_type = "test_interaction_type"
        self.event.value = 1234.56
        self.event.transaction = "test_transaction"
        self.event.properties = properties

        self.maxDiff = 10000

        self.assertEqual(
            self.event._payload,
            {
                "occurred": "2022-01-11T11:30:00",
                "user": {"named_user_id": "test_named_user"},
                "body": {
                    "name": "test_event",
                    "session_id": "0617a35e-b0c2-4b1c-9c41-586ca6b081d6",
                    "interaction_id": "test_interaction_id",
                    "interaction_type": "test_interaction_type",
                    "value": 1234.56,
                    "transaction": "test_transaction",
                    "properties": properties,
                },
            },
        )
