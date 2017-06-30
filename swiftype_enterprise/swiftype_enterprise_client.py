import requests
import time
from .exceptions import InvalidCredentials, NonExistentRecord, RecordAlreadyExists, BadRequest, Forbidden, InvalidDocument
from .utils import Timeout, windows_incompatible
from future.utils import lmap

"""API client for Swiftype Enterprise"""

class SwiftypeEnterpriseClient:

    SWIFTYPE_ENTERPRISE_API_BASE_URL = 'https://api.swiftype.com/api/v1/ent'

    REQUIRED_DOCUMENT_TOP_LEVEL_KEYS = [
        'external_id',
        'url',
        'title',
        'body'
    ]
    OPTIONAL_DOCUMENT_TOP_LEVEL_KEYS = [
        'created_at',
        'updated_at',
        'type'
    ]

    def __init__(self, authorization_token, base_url=SWIFTYPE_ENTERPRISE_API_BASE_URL):
        self.authorization_token = authorization_token
        self.base_url = base_url

    @windows_incompatible
    def index_documents(self, content_source_key, documents, **kwargs):
        """Creates or updates documents for a content source.
        Raises :class:`~swiftype_enterprise.SynchronousDocumentIndexingFailed`
        if the documents do not finish indexing when timeout expires.
        Raises :class:`~swiftype_enterprise.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises a
        :class:`~swiftype_enterprise.SwiftypeEnterpriseError` if there are any
        HTTP errors.

        :param content_source_key: Key for the content source.
        :param documents: Array of documents to be indexed.
        :param \**kwargs: See below.
        :return: Array of dicts that represent document receipts.

        :Keyword Arguments:
            *timeout* -- Number of seconds to wait for documents to finish
            indexing
            *delay* (``int``) -- Number of seconds to wait before checking
            if documents are done indexing

        >>> from swiftype_enterprise import SwiftypeEnterpriseClient
        >>> from swiftype_enterprise.exceptions import SynchronousDocumentIndexingFailed
        >>> content_source_key = 'content source key'
        >>> authorization_token = 'authorization token'
        >>> client = SwiftypeEnterpriseClient(authorization_token)
        >>> documents = [
            {
                'external_id': '1',
                'url': 'https://github.com/swiftype/swiftype-enterprise-python',
                'title': 'Swiftype Enterprise Python Github',
                'body': 'A descriptive body'
            }
        ]
        >>> try:
        >>>     document_receipt_ids = client.index_documents(content_source_key, documents, timeout=10, delay=2)
        >>>     print(document_receipt_ids)
        >>> except SynchronousDocumentIndexingFailed:
        >>>     # Timed out before documents could finish indexing
        [{'status': 'complete', 'errors': [], 'external_id': '1', 'id': 'doc_receipt_1', 'links': {'document_receipt': 'http://localhost:3002/api/v1/ent/document_receipts/5955d325f81eeace502f0a50'}}, ...]
        """
        response = self._async_create_or_update_documents(content_source_key,
                                                          documents)
        doc_receipt_ids = lmap(lambda x: x['id'],
                               response['document_receipts'])
        return self._poll_document_receipt_ids_for_completion(doc_receipt_ids,
                                                              **kwargs)

    def async_index_documents(self, content_source_key, documents):
        """Queues documents for to be created or updated in a content source.
        Raises :class:`~swiftype_enterprise.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises a
        :class:`~swiftype_enterprise.SwiftypeEnterpriseError` if there are any
        HTTP errors.

        :param content_source_key: Key for the content source.
        :param documents: Array of documents to be indexed.
        :return: Array of document receipt ids.

        >>> from swiftype_enterprise import SwiftypeEnterpriseClient
        >>> from swiftype_enterprise.exceptions import SwiftypeEnterpriseError
        >>> content_source_key = 'content source key'
        >>> authorization_token = 'authorization token'
        >>> client = SwiftypeEnterpriseClient(authorization_token)
        >>> documents = [
            {
                'external_id': '1',
                'url': 'https://github.com/swiftype/swiftype-enterprise-python',
                'title': 'Swiftype Enterprise Python Github',
                'body': 'A descriptive body'
            }
        ]
        >>> try:
        >>>     document_receipt_ids = client.async_index_documents(content_source_key, documents)
        >>>     print(document_receipt_ids)
        >>> except SwiftypeEnterpriseError:
        >>>     # handle exception
        ['5955d325f81eeace502f0a50']
        """
        response = self._async_create_or_update_documents(content_source_key,
                                                          documents)
        return lmap(lambda x: x['id'], response['document_receipts'])

    def document_receipts(self, document_receipt_ids):
        """Gets document receipts from their ids.
        Raises a :class:`~swiftype_enterprise.SwiftypeEnterpriseError` if there
        are any HTTP errors.

        :param document_receipt_ids: Array of document receipt ids.
        :return: Array of dicts that represent document receipts.

        >>> from swiftype_enterprise import SwiftypeEnterpriseClient
        >>> from swiftype_enterprise.exceptions import SwiftypeEnterpriseError
        >>> content_source_key = 'content source key'
        >>> authorization_token = 'authorization token'
        >>> client = SwiftypeEnterpriseClient(authorization_token)
        >>> try:
        >>>     document_receipts = client.document_receipts(['doc_receipt_1', 'doc_receipt_2'])
        >>>     print(document_receipts)
        >>> except SwiftypeEnterpriseError:
        >>>     # handle exception
        [{'status': 'complete', 'errors': [], 'external_id': '5955d325f81eeace502f0a50', 'id': 'doc_receipt_1', 'links': {'document_receipt': 'http://localhost:3002/api/v1/ent/document_receipts/doc_receipt_1'}}, ...]
        """
        return self._get_request('document_receipts/bulk_show.json',
                                 {'ids': ','.join(document_receipt_ids)})

    def destroy_documents(self, content_source_key, external_ids):
        """Destroys documents in a content source by their external_ids.
        Raises :class:`~swiftype_enterprise.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises a
        :class:`~swiftype_enterprise.SwiftypeEnterpriseError` if there are any
        HTTP errors.

        :param content_source_key: Key for the content source.
        :param external_ids: Array of document external ids to be destroyed.
        :return: Array of result dicts, with keys of `external_id` and `status`

        >>> from swiftype_enterprise import SwiftypeEnterpriseClient
        >>> from swiftype_enterprise.exceptions import SwiftypeEnterpriseError
        >>> content_source_key = 'content source key'
        >>> authorization_token = 'authorization token'
        >>> client = SwiftypeEnterpriseClient(authorization_token)
        >>> try:
        >>>     response = client.destroy_documents(content_source_key, ['1'])
        >>>     print(response)
        >>> except SwiftypeEnterpriseError:
        >>>     # handle exception
        [{"external_id": '1',"success": True}]
        """
        endpoint = "sources/{}/documents/bulk_destroy".format(
            content_source_key)
        return self._post_request(endpoint, external_ids)

    def _raise_if_error(self, response):
        if response.status_code == requests.codes.unauthorized:
            raise InvalidCredentials(response.reason)
        elif response.status_code == requests.codes.bad:
            raise BadRequest()
        elif response.status_code == requests.codes.conflict:
            raise RecordAlreadyExists()
        elif response.status_code == requests.codes.not_found:
            raise NonExistentRecord()
        elif response.status_code == requests.codes.forbidden:
            raise Forbidden()

        response.raise_for_status()

    def _request_helper(self, request_func, endpoint, **kwargs):
        url = "{}/{}".format(self.base_url, endpoint)
        headers = {
            'Authorization': "Bearer {}".format(self.authorization_token)
        }

        response = request_func(url, headers=headers, **kwargs)
        self._raise_if_error(response)

        return response.json()


    def _post_request(self, endpoint, payload=None):
        payload = payload or {}
        return self._request_helper(requests.post, endpoint, json=payload)

    def _get_request(self, endpoint, payload=None):
        payload = payload or {}
        return self._request_helper(requests.get, endpoint, params=payload)

    @windows_incompatible
    def _poll_document_receipt_ids_for_completion(self, document_receipt_ids,
                                                  timeout=10,
                                                  delay=0.5):
        with Timeout(seconds=timeout):
            while True:
                doc_receipts = self.document_receipts(document_receipt_ids)

                if all(lmap(lambda x: x['status'] != 'pending',
                                doc_receipts)):
                    return doc_receipts
                time.sleep(delay)
                delay *= 2

    def raise_if_document_invalid(self, document):
        missing_required_keys = set(self.REQUIRED_DOCUMENT_TOP_LEVEL_KEYS) - set(document.keys())
        if len(missing_required_keys):
            raise InvalidDocument(
                "Missing required fields: {}".format(','.join(missing_required_keys)),
                document
            )

        invalid_fields = set(document.keys()) - set(self.REQUIRED_DOCUMENT_TOP_LEVEL_KEYS + self.OPTIONAL_DOCUMENT_TOP_LEVEL_KEYS)
        if len(invalid_fields):
            raise InvalidDocument(
                "Invalid fields in document: {}".format(
                    ', '.join(invalid_fields)
                ),
                document
            )
            
    def _async_create_or_update_documents(self, content_source_key, documents):
        for document in documents:
            self.raise_if_document_invalid(document)
        endpoint = "sources/{}/documents/bulk_create".format(content_source_key)
        return self._post_request(endpoint, documents)
