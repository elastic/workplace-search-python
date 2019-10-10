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
        response = {}

        # Test that index_documents proxies through to Documents service.
        with patch('elastic_enterprise_search.apis.documents.Documents.index_documents', return_value=response) as index_documents:
            return_value = self.client.index_documents(content_source_key, documents)
            index_documents.assert_called_with(content_source_key, documents)
            self.assertEqual(return_value, response)

    def test_destroy_documents(self):
        content_source_key = 'key'
        ids = ['some_id']
        response = [
            {
                'id': '1',
                'success': True
            }
        ]

        # Test that delete_documents proxies through to Documents service.
        with patch('elastic_enterprise_search.apis.documents.Documents.delete_documents', return_value=response) as delete_documents:
            return_value = self.client.destroy_documents(content_source_key, ids)
            delete_documents.assert_called_with(content_source_key, ids)
            self.assertEqual(return_value, response)
