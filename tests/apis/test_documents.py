from unittest import TestCase
from requests.status_codes import codes

try:  # python 3.3+
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from .mock_endpoint import mock_endpoint
from elastic_enterprise_search.client import Client
from .fixtures.index_documents_response import *
from .fixtures.delete_documents_response import *


class TestDocuments(TestCase):

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

        def test_request(request_properties):
            actual_json = request_properties.pop('json')
            expected_json = documents
            self.assertEqual(actual_json, expected_json)

        mocked_endpoint = mock_endpoint(
            'post',
            'sources/{}/documents/bulk_create'.format(content_source_key),
            index_documents_response,
            test_request
        )

        with patch(**mocked_endpoint):
            response = self.client.documents.index_documents('key', documents)
            self.assertEqual(response.__len__(), 2)

    def test_delete_documents(self):
        content_source_key = 'key'
        ids = ['1']

        def test_request(request_properties):
            actual_json = request_properties.pop('json')
            expected_json = ids
            self.assertEqual(actual_json, expected_json)

        mocked_endpoint = mock_endpoint(
            'post',
            'sources/{}/documents/bulk_destroy'.format(content_source_key),
            delete_documents_response,
            test_request
        )

        with patch(**mocked_endpoint):
            self.assertEqual(
                self.client.documents.delete_documents(
                    content_source_key, ids),
                delete_documents_response
            )
