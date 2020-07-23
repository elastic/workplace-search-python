import os
import pytest
from elastic_workplace_search import Client


if "ENT_SEARCH_CREDS" in os.environ:
    ENT_SEARCH_CREDS = os.environ["ENT_SEARCH_CREDS"].split(":")
else:
    ENT_SEARCH_CREDS = (
        "5eebbb1e5e21d6c1e64f9578",
        "32744aeb04f1269f57376347ee1d8f4e915e8273bfa9b2036aff4ef770bd2377",
    )


@pytest.fixture(scope="session")
def client():
    return Client(
        authorization_token=ENT_SEARCH_CREDS[1],
        base_url="http://localhost:8080/api/ws/v1",
    )


@pytest.fixture(scope="session")
def content_source_key(client):
    return ENT_SEARCH_CREDS[0]
