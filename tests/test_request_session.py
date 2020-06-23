import pytest
from requests.status_codes import codes
from mock import MagicMock, patch

import elastic_workplace_search
from elastic_workplace_search.request_session import RequestSession
from elastic_workplace_search.exceptions import InvalidCredentials


class TestRequestSession:

    dummy_authorization_token = "authorization_token"

    def test_request_success(self):
        http = RequestSession(self.dummy_authorization_token, "base_url")

        expected_return = {"foo": "bar"}
        stubbed_return = MagicMock(status_code=codes.ok, json=lambda: expected_return)
        with patch("requests.Session.request", return_value=stubbed_return):
            resp = http.request("post", "http://doesnt.matter.org")

        assert resp == expected_return

    def test_headers_initialization(self):
        http = RequestSession(self.dummy_authorization_token, "base_url")
        headers = dict(http.session.headers.items())
        version = elastic_workplace_search.__version__

        assert headers == {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Authorization": "Bearer authorization_token",
            "Connection": "keep-alive",
            "User-Agent": "python-requests/2.24.0",
            "X-Swiftype-Client": "elastic-workplace-search-python",
            "X-Swiftype-Client-Version": version,
        }

    def test_request_throw_error(self):
        http = RequestSession(self.dummy_authorization_token, "base_url")
        stubbed_return = MagicMock(status_code=codes.unauthorized)

        with patch("requests.Session.request", return_value=stubbed_return):
            with pytest.raises(InvalidCredentials):
                http.request("post", "http://doesnt.matter.org")
