import unittest

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestAirshipUrls(unittest.TestCase):
    def setUp(self):
        self.us_airship = ua.Airship(TEST_KEY, TEST_SECRET, location='us')
        self.eu_airship = ua.Airship(TEST_KEY, TEST_SECRET, location='eu')

    def test_us_url(self):
        base_url = 'https://go.urbanairship.com/api/'
        self.assertEqual(
            self.us_airship.urls.get('base_url'),
            base_url
        )

    def test_eu_url(self):
        base_url = 'https://go.airship.eu/api/'
        self.assertEqual(
            self.eu_airship.urls.get('base_url'),
            base_url
        )