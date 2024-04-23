import unittest

from tests import TEST_KEY, TEST_SECRET, TEST_TOKEN
from urbanairship.client import BearerTokenClient


class TestTokenClient(unittest.TestCase):
    def test_token_client_timeout(self):
        timeout_int = 50

        airship_timeout = BearerTokenClient(
            key=TEST_KEY, token=TEST_TOKEN, timeout=timeout_int
        )

        self.assertEqual(airship_timeout.timeout, timeout_int)

    def test_token_client_timeout_exception(self):
        timeout_str = "50"

        with self.assertRaises(ValueError):
            BearerTokenClient(key=TEST_KEY, token=TEST_TOKEN, timeout=timeout_str)

    def test_token_client_retry(self):
        retry_int = 5

        airship_w_retry = BearerTokenClient(TEST_KEY, TEST_SECRET, retries=retry_int)

        self.assertEqual(retry_int, airship_w_retry.retries)

    def test_token_client_location(self):
        location = "eu"

        airship_eu = BearerTokenClient(
            key=TEST_KEY, token=TEST_TOKEN, location=location
        )

        self.assertEqual(airship_eu.location, location)

    def test_token_client_location_exception(self):
        invalid_location = "xx"

        with self.assertRaises(ValueError):
            BearerTokenClient(key=TEST_KEY, token=TEST_TOKEN, location=invalid_location)

    def test_token_auth(self):
        test_token_client = BearerTokenClient(key=TEST_KEY, token=TEST_TOKEN)

        self.assertEqual(TEST_TOKEN, test_token_client.token)
