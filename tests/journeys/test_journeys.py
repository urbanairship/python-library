import json
import unittest

import mock
import requests

import urbanairship as ua
from tests import TEST_KEY
from urbanairship.client import OAuthClient

PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"


def make_oauth_client():
    return OAuthClient(
        key=TEST_KEY,
        client_id=TEST_KEY,
        private_key=PRIVATE_KEY,
    )


def ok_response():
    response = requests.Response()
    response._content = json.dumps(
        {"ok": True, "operation_id": "d67d4de6-934f-4ebb-aef0-250d89699b6b"}
    ).encode("utf-8")
    response.status_code = 200
    return response


class TestJourneys(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.airship = make_oauth_client()
        self.journeys = ua.Journeys(self.airship)

    def test_requires_oauth_client(self):
        basic = ua.BasicAuthClient(TEST_KEY, TEST_KEY)
        with self.assertRaises(TypeError):
            ua.Journeys(basic)

    def test_trigger_minimal(self):
        with mock.patch.object(OAuthClient, "_request") as mock_request:
            mock_request.return_value = ok_response()

            result = self.journeys.trigger(
                audience=ua.tag("breakfast_buyers"),
                triggering_id="test-triggering-id",
            )

            self.assertTrue(result["ok"])
            method, body, url = mock_request.call_args.args[:3]
            self.assertEqual(method, "POST")
            self.assertEqual(url, self.airship.urls.get("journeys_trigger_url"))
            self.assertEqual(
                json.loads(body),
                {
                    "audience": {"tag": "breakfast_buyers"},
                    "triggering_id": "test-triggering-id",
                },
            )

    def test_trigger_full(self):
        with mock.patch.object(OAuthClient, "_request") as mock_request:
            mock_request.return_value = ok_response()

            self.journeys.trigger(
                audience=ua.or_(ua.tag("a"), ua.tag("b")),
                triggering_id=["id-1", "id-2"],
                entrance_id="entrance-1",
                global_attributes={"category": "mens shoes"},
            )

            body = mock_request.call_args.args[1]
            self.assertEqual(
                json.loads(body),
                {
                    "audience": {"or": [{"tag": "a"}, {"tag": "b"}]},
                    "triggering_id": ["id-1", "id-2"],
                    "entrance_id": "entrance-1",
                    "global_attributes": {"category": "mens shoes"},
                },
            )

    def test_exit_minimal(self):
        with mock.patch.object(OAuthClient, "_request") as mock_request:
            mock_request.return_value = ok_response()

            result = self.journeys.exit(triggering_id="test-triggering-id")

            self.assertTrue(result["ok"])
            method, body, url = mock_request.call_args.args[:3]
            self.assertEqual(method, "POST")
            self.assertEqual(url, self.airship.urls.get("journeys_exit_url"))
            self.assertEqual(
                json.loads(body),
                {"triggering_id": "test-triggering-id"},
            )

    def test_exit_full(self):
        with mock.patch.object(OAuthClient, "_request") as mock_request:
            mock_request.return_value = ok_response()

            self.journeys.exit(
                triggering_id=["id-1", "id-2"],
                entrance_id="entrance-1",
            )

            body = mock_request.call_args.args[1]
            self.assertEqual(
                json.loads(body),
                {
                    "triggering_id": ["id-1", "id-2"],
                    "entrance_id": "entrance-1",
                },
            )

    def test_triggering_id_list_too_long(self):
        with self.assertRaises(ValueError):
            self.journeys.exit(triggering_id=[str(i) for i in range(11)])

    def test_triggering_id_empty_list(self):
        with self.assertRaises(ValueError):
            self.journeys.exit(triggering_id=[])

    def test_triggering_id_invalid_type(self):
        with self.assertRaises(TypeError):
            self.journeys.exit(triggering_id=123)


if __name__ == "__main__":
    unittest.main()
