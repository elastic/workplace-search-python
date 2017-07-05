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
from swiftype_enterprise.exceptions import InvalidCredentials, SynchronousDocumentIndexingFailed, InvalidDocument

class TestSwiftypeEnterpriseClient(TestCase):
    dummy_authorization_token = 'authorization_token'

    def setUp(self):
        self.client = SwiftypeEnterpriseClient('authorization_token')

    def test_request_success(self):
        expected_return = {'foo': 'bar'}
        stubbed_return = MagicMock(status_code=codes.ok,
                                   json=lambda: expected_return)
        with patch('requests.post', return_value=stubbed_return):
            response = self.client._post_request('http://doesnt.matter.org')
            self.assertEqual(response, expected_return)

    def test_request_authetication(self):
        stubbed_return = MagicMock(status_code=codes.ok,
                                   json=lambda: {})

        def verify_authorization_header(*args, **kwargs):
            self.assertEqual(
                kwargs.pop('headers')['Authorization'],
                "Bearer {}".format(self.dummy_authorization_token)
            )
            return stubbed_return

        with patch('requests.post', side_effect=verify_authorization_header):
            self.client._post_request('http://doesnt.matter.org')

    def test_request_throw_error(self):
        stubbed_return = MagicMock(status_code=codes.unauthorized)
        with patch('requests.post', return_value=stubbed_return):
            with self.assertRaises(InvalidCredentials) as _context:
                self.client._post_request('http://doesnt.matter.org')

    def test_document_receipts(self):
        document_receipt_ids = ['1', '2']
        stubbed_response = MagicMock(status_code=codes.ok, json=lambda: None)
        expected_endpoint = "{}/{}".format(self.client.SWIFTYPE_ENTERPRISE_API_BASE_URL,
                                           'document_receipts/bulk_show.json')
        def side_effect(*args, **kwargs):
            self.assertEqual(expected_endpoint, args[0])
            self.assertEqual(kwargs.pop('params').get('ids'),
                             ','.join(document_receipt_ids))
            return stubbed_response

        with patch('requests.get', side_effect=side_effect):
            self.client.document_receipts(document_receipt_ids)

        external_id = 1
        title, body, url = 'title', 'body', 'url'
        response_body = [
            {
                "external_id" : external_id,
                "title": title,
                "body": body,
                "url": url
            }
        ]
        status = 'pending'
        document_receipt_id = 'document_receipt_id'
        response_body = {
            'batch_link': 'blah',
            'document_receipts': [
                {
                    'id': document_receipt_id,
                    'external_id': '1',
                    'status': status,
                    'document_receipt': 'some url'
                }
            ]
        }
        stubbed_response = MagicMock(status_code=codes.ok,
                                     json=lambda: response_body)
        with patch('requests.get', return_value=stubbed_response):
            response = self.client.document_receipts([document_receipt_id])
            self.assertEqual(response, response_body)

    def test_async_index_documents(self):
        content_source_key = 'key'
        documents = [
            {
                'external_id': 1,
                'url': '',
                'title': '',
                'body': ''
            },
            {
                'external_id': 2,
                'url': '',
                'title': '',
                'body': ''
            }
        ]
        stubbed_response = MagicMock(status_code=codes.ok,
                                     json=lambda: {'document_receipts': []})
        expected_endpoint = "{}/sources/{}/documents/bulk_create"\
            .format(self.client.SWIFTYPE_ENTERPRISE_API_BASE_URL,
                    content_source_key)

        def side_effect(*args, **kwargs):
            self.assertEqual(expected_endpoint, args[0])
            self.assertEqual(kwargs.pop('json'), documents)
            return stubbed_response

        with patch('requests.post', side_effect=side_effect):
            self.client.async_index_documents(content_source_key, documents)

        document_receipt_ids = ['1', '2']
        response_body = {
            'document_receipts': lmap(lambda x: {'id': x}, document_receipt_ids)
        }
        stubbed_response = MagicMock(status_code=codes.ok,
                                     json=lambda: response_body)

        with patch('requests.post', return_value=stubbed_response):
            self.assertEqual(
                self.client.async_index_documents('key', documents),
                document_receipt_ids)

        invalid_document = {
            'bad': 'document'
        }
        with self.assertRaises(InvalidDocument) as _context:
            self.client.async_index_documents('key', [invalid_document])

    def test_raise_if_document_invalid(self):
        valid_document = {
            'external_id': 'external_id',
            'url': 'url',
            'title': 'title',
            'body': 'body',
            'created_at': 'created_at'
        }

        self.client.raise_if_document_invalid(valid_document)

        invalid_document = {
            'external_id': 'external_id',
            'title': 'title',
            'body': 'body',
            'created_at': 'created_at'
        }

        with self.assertRaises(InvalidDocument) as context:
            self.client.raise_if_document_invalid(invalid_document)

        self.assertEqual(context.exception.document, invalid_document)
        self.assertIn('url', context.exception.args[0])

        document_with_invalid_key = {
            'external_id': 'external_id',
            'url': 'url',
            'title': 'title',
            'body': 'body',
            'bad_key': 'bad_key'
        }

        with self.assertRaises(InvalidDocument) as bad_key_context:
            self.client.raise_if_document_invalid(document_with_invalid_key)

        self.assertEqual(bad_key_context.exception.document, document_with_invalid_key)
        self.assertIn('bad_key', bad_key_context.exception.args[0])

    @skipIf(platform.system() == 'Windows', 'Not Windows compatible')
    def test_poll_document_receipt_ids_for_completion(self):

        with self.assertRaises(SynchronousDocumentIndexingFailed) as _context:

            def slow_side_effect(*args, **kwargs):
                time.sleep(20)

            with patch('requests.get', side_effect=slow_side_effect):
                self.client._poll_document_receipt_ids_for_completion([], 1)

        pending_document_receipts_response = [
            {
                'id': 'some_id',
                'status': 'pending'
            }
        ] * 2
        stubbed_response = MagicMock(status_code=codes.ok,
                                     json=lambda: pending_document_receipts_response)
        with self.assertRaises(SynchronousDocumentIndexingFailed) as _context:
            with patch('requests.get', side_effect=cycle([stubbed_response])):
                self.client._poll_document_receipt_ids_for_completion([], 1)

        document_receipt_id = 'doc_receipt_id'
        response_body_1 = [
            {
                'id': document_receipt_id,
                'status': 'pending'
            }
        ]
        response_body_2 = [
            {
                'id': document_receipt_id,
                'status': 'complete'
            }
        ]
        stubbed_response_1 = MagicMock(status_code=codes.ok,
                                   json=lambda: response_body_1)
        stubbed_response_2 = MagicMock(status_code=codes.ok,
                               json=lambda: response_body_2)

        with patch('requests.get', side_effect=[stubbed_response_1, stubbed_response_2]):
            self.assertEqual(
                self.client._poll_document_receipt_ids_for_completion(['some_receipt_id'], 2),
                response_body_2
            )

    @skipIf(platform.system() == 'Windows', 'Not Windows compatible')
    def test_index_documents(self):
        content_source_key = 'key'
        documents = [
            {
                'external_id': 1,
                'url': '',
                'title': '',
                'body': ''
            }
        ]
        bulk_create_docs_response = {
            'document_receipts': [
                 {
                     'id': 'some_id',
                     'status': 'complete'
                 }
             ]
        }
        doc_receipts_response = bulk_create_docs_response['document_receipts']

        bulk_create_docs_stubbed_response = MagicMock(status_code=codes.ok,
                                                      json=lambda: bulk_create_docs_response)
        doc_receipts_stubbed_response = MagicMock(status_code=codes.ok,
                                                       json=lambda: doc_receipts_response)

        # stub documents bulk_create endpoint
        with patch('requests.post', return_value=bulk_create_docs_stubbed_response):
            # stub document receipts bulk_show endpoint
            with patch('requests.get', return_value=doc_receipts_stubbed_response):
                self.assertEqual(
                    self.client.index_documents(content_source_key, documents),
                    doc_receipts_response
                )

        with patch('platform.system', return_value='Windows'):
            with self.assertRaises(OSError) as context:
                self.client.index_documents(content_source_key, documents)
            self.assertIn('Please use `async_index_documents` instead', context.exception.args[0])

    def test_destroy_documents(self):
        content_source_key = 'key'
        external_ids = ['some_id']
        response_body = [
            {
                'external_id': '1',
                'success': True
            }
        ]
        stubbed_response = MagicMock(status_code=codes.ok,
                                     json=lambda: response_body)
        with patch('requests.post', return_value=stubbed_response):
            self.assertEqual(
                self.client.destroy_documents(content_source_key, external_ids),
                response_body
            )
