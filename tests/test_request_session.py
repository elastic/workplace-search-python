from unittest import TestCase, skipIf
from requests.status_codes import codes
from future.utils import iteritems

try:  # python 3.3+
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

import elastic_workplace_search
from elastic_workplace_search.request_session import RequestSession
from elastic_workplace_search.exceptions import InvalidCredentials


class TestRequestSession(TestCase):

    dummy_authorization_token = 'authorization_token'

    def setUp(self):
        self.session = RequestSession(self.dummy_authorization_token, 'base_url')

    def test_request_success(self):
        expected_return = {'foo': 'bar'}
        stubbed_return = MagicMock(status_code=codes.ok,
                                   json=lambda: expected_return)
        with patch('requests.Session.request', return_value=stubbed_return):
            response = self.session.request('post', 'http://doesnt.matter.org')
            self.assertEqual(response, expected_return)

    def test_headers_initialization(self):
        headers_to_check = {
            k: v
            for k, v in iteritems(self.session.session.headers)
            if k in ['Authorization', 'X-Swiftype-Client', 'X-Swiftype-Client-Version']
        }
        version = elastic_workplace_search.__version__
        self.assertEqual(
            headers_to_check,
            {
                'Authorization': 'Bearer {}'.format(self.dummy_authorization_token),
                'X-Swiftype-Client': 'elastic-workplace-search-python',
                'X-Swiftype-Client-Version': '0.2.0',
            }
        )

    def test_request_throw_error(self):
        stubbed_return = MagicMock(status_code=codes.unauthorized)
        with patch('requests.Session.request', return_value=stubbed_return):
            with self.assertRaises(InvalidCredentials) as _context:
                self.session.request('post', 'http://doesnt.matter.org')
