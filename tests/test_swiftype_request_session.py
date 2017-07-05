from unittest import TestCase, skipIf
from requests.status_codes import codes
from future.utils import iteritems

try:  # python 3.3+
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

import swiftype_enterprise
from swiftype_enterprise.swiftype_request_session import SwiftypeRequestSession
from swiftype_enterprise.exceptions import InvalidCredentials, SynchronousDocumentIndexingFailed, InvalidDocument


class TestSwiftypeRequestSession(TestCase):

    dummy_authorization_token = 'authorization_token'

    def setUp(self):
        self.swiftype_session = SwiftypeRequestSession(self.dummy_authorization_token, 'base_url')

    def test_request_success(self):
        expected_return = {'foo': 'bar'}
        stubbed_return = MagicMock(status_code=codes.ok,
                                   json=lambda: expected_return)
        with patch('requests.Session.request', return_value=stubbed_return):
            response = self.swiftype_session.request('post', 'http://doesnt.matter.org')
            self.assertEqual(response, expected_return)

    def test_headers_initialization(self):
        headers_to_check = {
            k: v
            for k, v in iteritems(self.swiftype_session.session.headers)
            if k in ['Authorization', 'User-Agent']
        }
        version = swiftype_enterprise.__version__
        self.assertEqual(
            headers_to_check,
            {
                'Authorization': 'Bearer {}'.format(self.dummy_authorization_token),
                'User-Agent': 'swiftype-enterprise-python/{}'.format(version)
            }
        )

    def test_request_throw_error(self):
        stubbed_return = MagicMock(status_code=codes.unauthorized)
        with patch('requests.Session.request', return_value=stubbed_return):
            with self.assertRaises(InvalidCredentials) as _context:
                self.swiftype_session.request('post', 'http://doesnt.matter.org')