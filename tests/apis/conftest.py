import pytest
from elastic_workplace_search import Client


@pytest.fixture(scope="session")
def vcr_config():
    return {"filter_headers": ["user-agent"]}


@pytest.fixture(scope="session")
def client():
    return Client(
        authorization_token=(
            "32744aeb04f1269f57376347ee1d8f4e915e8273bfa9b2036aff4ef770bd2377"
        ),
        base_url="http://localhost:8080/api/ws/v1",
    )


@pytest.fixture(scope="session")
def content_source_key(client):
    return "5eebbb1e5e21d6c1e64f9578"
