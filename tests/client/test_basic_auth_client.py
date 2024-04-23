import unittest

from tests import TEST_KEY, TEST_SECRET
from urbanairship.client import BasicAuthClient


class TestBasicClient(unittest.TestCase):
    def test_basic_client_timeout(self):
        timeout_int = 50

        airship_timeout = BasicAuthClient(
            key=TEST_KEY, secret=TEST_SECRET, timeout=timeout_int
        )

        self.assertEqual(airship_timeout.timeout, timeout_int)

    def test_basic_client_timeout_exception(self):
        timeout_str = "50"

        with self.assertRaises(ValueError):
            BasicAuthClient(key=TEST_KEY, secret=TEST_SECRET, timeout=timeout_str)

    def test_basic_client_retry(self):
        retry_int = 5

        airship_w_retry = BasicAuthClient(TEST_KEY, TEST_SECRET, retries=retry_int)

        self.assertEqual(retry_int, airship_w_retry.retries)

    def test_basic_client_location(self):
        location = "eu"

        airship_eu = BasicAuthClient(
            key=TEST_KEY, secret=TEST_SECRET, location=location
        )

        self.assertEqual(airship_eu.location, location)

    def test_basic_client_location_exception(self):
        invalid_location = "xx"

        with self.assertRaises(ValueError):
            BasicAuthClient(key=TEST_KEY, secret=TEST_SECRET, location=invalid_location)
