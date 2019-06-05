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

from swiftype_enterprise.swiftype_enterprise_client import SwiftypeEnterpriseClient
from swiftype_enterprise.exceptions import SynchronousDocumentIndexingFailed, InvalidDocument

class TestSwiftypeEnterpriseClient(TestCase):
    dummy_authorization_token = 'authorization_token'

    def setUp(self):
        self.client = SwiftypeEnterpriseClient('authorization_token')


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
            .format(self.client.SWIFTYPE_ENTERPRISE_API_BASE_URL,
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

        invalid_document = {
            'bad': 'document'
        }
        with self.assertRaises(InvalidDocument) as _context:
            self.client.index_documents('key', [invalid_document])

    def test_raise_if_document_invalid(self):
        valid_document = {
            'id': 'id',
            'url': 'url',
            'title': 'title',
            'body': 'body',
            'created_at': 'created_at'
        }

        self.client.raise_if_document_invalid(valid_document)

        invalid_document = {
            'id': 'id',
            'title': 'title',
            'body': 'body',
            'created_at': 'created_at'
        }

        with self.assertRaises(InvalidDocument) as context:
            self.client.raise_if_document_invalid(invalid_document)

        self.assertEqual(context.exception.document, invalid_document)
        self.assertIn('url', context.exception.args[0])

        document_with_invalid_key = {
            'id': 'id',
            'url': 'url',
            'title': 'title',
            'body': 'body',
            'bad_key': 'bad_key'
        }

        with self.assertRaises(InvalidDocument) as bad_key_context:
            self.client.raise_if_document_invalid(document_with_invalid_key)

        self.assertEqual(bad_key_context.exception.document, document_with_invalid_key)
        self.assertIn('bad_key', bad_key_context.exception.args[0])

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
