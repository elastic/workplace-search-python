import time
from .swiftype_request_session import SwiftypeRequestSession
from .utils import Timeout, windows_incompatible
from future.utils import lmap

"""API client for Swiftype Enterprise"""

class SwiftypeEnterpriseClient:

    SWIFTYPE_ENTERPRISE_API_BASE_URL = 'http://localhost:3002/api/v1/ent'

    def __init__(self, authorization_token, base_url=SWIFTYPE_ENTERPRISE_API_BASE_URL):
        self.authorization_token = authorization_token
        self.base_url = base_url
        self.swiftype_session = SwiftypeRequestSession(self.authorization_token, self.base_url)

    def index_documents(self, content_source_key, documents, **kwargs):
        """Index a batch of documents in a content source.
        Raises :class:`~swiftype_enterprise.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises
        :class:`~swiftype_enterprise.SwiftypeEnterpriseError` if there are any
        HTTP errors.

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
                'id': '1',
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
        [{'errors': [], 'id': '1', 'id': None}]
        """
        return self._async_create_or_update_documents(content_source_key,
                                                          documents)

    def destroy_documents(self, content_source_key, ids):
        """Destroys documents in a content source by their ids.
        Raises :class:`~swiftype_enterprise.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises
        :class:`~swiftype_enterprise.SwiftypeEnterpriseError` if there are any
        HTTP errors.

        :param content_source_key: Key for the content source.
        :param ids: Array of document ids to be destroyed.
        :return: Array of result dicts, with keys of `id` and `status`

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
        [{"id": '1',"success": True}]
        """
        endpoint = "sources/{}/documents/bulk_destroy".format(
            content_source_key)
        return self.swiftype_session.request('post', endpoint, json=ids)


    def _async_create_or_update_documents(self, content_source_key, documents):
        endpoint = "sources/{}/documents/bulk_create".format(content_source_key)
        return self.swiftype_session.request('post', endpoint, json=documents)
