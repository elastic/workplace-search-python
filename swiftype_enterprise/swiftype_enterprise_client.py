import time
from .exceptions import InvalidDocument, SynchronousDocumentIndexingFailed
from .swiftype_request_session import SwiftypeRequestSession
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
        self.swiftype_session = SwiftypeRequestSession(self.authorization_token, self.base_url)

    def index_documents(self, content_source_key, documents, **kwargs):
        """Index a batch of documents in a content source.
        Raises :class:`~swiftype_enterprise.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises
        :class:`~swiftype_enterprise.SwiftypeEnterpriseError` if there are any
        HTTP errors. Raises :class:`~swiftype_enterprise.InvalidDocument` when
        a document is missing required fields or contains unsupported fields.

        :param content_source_key: Key for the content source.
        :param documents: Array of documents to be indexed.
        :return: Array of document indexing results.

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
        >>>     document_results = client.index_documents(content_source_key, documents)
        >>>     print(document_results)
        >>> except SwiftypeEnterpriseError:
        >>>     # handle exception
        >>>     pass
        [{'errors': [], 'external_id': '1', 'id': None}]
        """
        return self._async_create_or_update_documents(content_source_key,
                                                          documents)

    def destroy_documents(self, content_source_key, external_ids):
        """Destroys documents in a content source by their external_ids.
        Raises :class:`~swiftype_enterprise.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises
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
        >>>     pass
        [{"external_id": '1',"success": True}]
        """
        endpoint = "sources/{}/documents/bulk_destroy".format(
            content_source_key)
        return self.swiftype_session.request('post', endpoint, json=external_ids)

    def raise_if_document_invalid(self, document):
        missing_required_keys = set(self.REQUIRED_DOCUMENT_TOP_LEVEL_KEYS) - set(document.keys())
        if len(missing_required_keys):
            raise InvalidDocument(
                "Missing required fields: {}".format(','.join(missing_required_keys)),
                document
            )

        core_top_level_keys = self.REQUIRED_DOCUMENT_TOP_LEVEL_KEYS + self.OPTIONAL_DOCUMENT_TOP_LEVEL_KEYS
        invalid_fields = set(document.keys()) - set(core_top_level_keys)
        if len(invalid_fields):
            raise InvalidDocument(
                "Invalid fields in document: {}".format(
                    ', '.join(invalid_fields)
                ) + ', ' +
                "supported fields are {}".format(', '.join(core_top_level_keys)),
                document
            )

    def _async_create_or_update_documents(self, content_source_key, documents):
        for document in documents:
            self.raise_if_document_invalid(document)
        endpoint = "sources/{}/documents/bulk_create".format(content_source_key)
        return self.swiftype_session.request('post', endpoint, json=documents)
