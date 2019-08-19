from unittest import TestCase, skipIf
from requests.status_codes import codes
from future.utils import lmap
import time
from itertools import cycle
import platform

try:  # python 3.3+
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from elastic_enterprise_search.client import Client

class TestClient(TestCase):
    dummy_authorization_token = 'authorization_token'

    def setUp(self):
        self.client = Client('authorization_token')


    def test_index_documents(self):
        content_source_key = 'key'
        documents = [
            {
                'id': 1,
                'url': '',
                'title': '',
                'body': ''
            },
            {
                'id': 2,
                'url': '',
                'title': '',
                'body': ''
            }
        ]
        response_body = [{'errors': [], 'id': '1', 'id': None},
                                     {'errors': [], 'id': '2', 'id': None}]
        stubbed_response = MagicMock(status_code=codes.ok,
                                     json=lambda: response_body)
        expected_endpoint = "{}/sources/{}/documents/bulk_create"\
            .format(self.client.ELASTIC_ENTERPRISE_SEARCH_BASE_URL,
                    content_source_key)

        def side_effect(*args, **kwargs):
            self.assertEqual('post', args[0])
            self.assertEqual(expected_endpoint, args[1])
            self.assertEqual(kwargs.pop('json'), documents)
            return stubbed_response

        with patch('requests.Session.request', side_effect=side_effect):
            self.client.index_documents(content_source_key, documents)

        with patch('requests.Session.request', return_value=stubbed_response):
            self.assertEqual(
                self.client.index_documents('key', documents),
                response_body)

    def test_destroy_documents(self):
        content_source_key = 'key'
        ids = ['some_id']
        response_body = [
            {
                'id': '1',
                'success': True
            }
        ]
        stubbed_response = MagicMock(status_code=codes.ok,
                                     json=lambda: response_body)
        with patch('requests.Session.request', return_value=stubbed_response):
            self.assertEqual(
                self.client.destroy_documents(content_source_key, ids),
                response_body
            )
