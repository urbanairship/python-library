import unittest

from urbanairship.urls import Urls


class TestAirshipUrls(unittest.TestCase):
    def setUp(self):
        self.test_url = "https://something.tld"
        return super().setUp()

    def test_no_location(self):
        urls = Urls()
        # use of apid_url is arbitrary
        self.assertIn("urbanairship.com", urls.apid_url)

    def test_no_location_oauth(self):
        urls = Urls(oauth_base=True)
        self.assertIn("asnapius.com", urls.apid_url)

    def test_us_location(self):
        urls = Urls(location="us")
        self.assertIn("urbanairship.com", urls.apid_url)

    def test_us_location_oauth(self):
        urls = Urls(location="us", oauth_base=True)
        self.assertIn("asnapius.com", urls.apid_url)

    def test_eu_location(self):
        urls = Urls(location="eu")
        self.assertIn("airship.eu", urls.apid_url)

    def test_eu_location_oauth(self):
        urls = Urls(location="eu", oauth_base=True)
        self.assertIn("asnapieu.com", urls.apid_url)

    def test_base_url(self):
        urls = Urls(base_url=self.test_url)
        self.assertEqual(urls.base_url, self.test_url)
        self.assertIn(self.test_url, urls.apid_url)
