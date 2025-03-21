import unittest

from tests import TEST_KEY
from urbanairship.client import OAuthClient


class TestOAuthClient(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = ["nu"]
        self.ip_addr = ["24.20.40.0/24"]
        self.timeout = 50
        self.retries = 3
        self.private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"

        self.test_oauth_client = OAuthClient(
            client_id=TEST_KEY,
            private_key=self.private_key,
            key=TEST_KEY,
            scope=self.scope,
            ip_addr=self.ip_addr,
            timeout=self.timeout,
            retries=self.retries,
        )

    def test_oauth_client_timeout(self):
        self.assertEqual(self.test_oauth_client.timeout, self.timeout)

    def test_oauth_client_id(self):
        self.assertEqual(self.test_oauth_client.client_id, TEST_KEY)

    def test_oauth_client_scope(self):
        self.assertEqual(self.test_oauth_client.scope, self.scope)

    def test_oauth_client_ip_addr(self):
        self.assertEqual(self.test_oauth_client.ip_addr, self.ip_addr)

    def test_oauth_client_retry(self):
        self.assertEqual(self.test_oauth_client.retries, self.retries)

    def test_oauth_token_url(self):
        self.assertEqual(
            self.test_oauth_client.token_url, "https://oauth2.asnapius.com/token"
        )

    def test_oauth_private_key(self):
        self.assertIn("-----BEGIN PRIVATE KEY-----", self.test_oauth_client.private_key)
        self.assertIn("-----END PRIVATE KEY-----", self.test_oauth_client.private_key)
