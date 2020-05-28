from unittest import TestCase

from elastic_workplace_search.client import Client


class TestClient(TestCase):
    dummy_authorization_token = "authorization_token"

    def setUp(self):
        self.client = Client("authorization_token")

    def test_constructor(self):
        self.assertIsInstance(self.client, Client)
