from elastic_workplace_search.client import Client


class TestClient:
    dummy_authorization_token = "authorization_token"

    def test_constructor(self):
        client = Client(self.dummy_authorization_token)
        assert isinstance(client, Client)
