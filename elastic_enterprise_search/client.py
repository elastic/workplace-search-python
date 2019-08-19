import time
from .request_session import RequestSession
from .utils import Timeout, windows_incompatible
from future.utils import lmap

"""API client for Elastic Enterprise Search"""

class Client:

    ELASTIC_ENTERPRISE_SEARCH_BASE_URL = 'http://localhost:3002/api/v1/ent'

    def __init__(self, authorization_token, base_url=ELASTIC_ENTERPRISE_SEARCH_BASE_URL):
        self.authorization_token = authorization_token
        self.base_url = base_url
        self.session = RequestSession(self.authorization_token, self.base_url)

    def index_documents(self, content_source_key, documents, **kwargs):
        """Index a batch of documents in a content source.
        Raises :class:`~elastic_enterprise_search.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises
        :class:`~elastic_enterprise_search.EnterpriseSearchError` if there are any
        HTTP errors.

        :param content_source_key: Key for the content source.
        :param documents: Array of documents to be indexed.
        :return: Array of document indexing results.

        >>> from elastic_enterprise_search import Client
        >>> from elastic_enterprise_search.exceptions import EnterpriseSearchError
        >>> content_source_key = 'content source key'
        >>> authorization_token = 'authorization token'
        >>> client = Client(authorization_token)
        >>> documents = [
            {
                'id': '1',
                'url': 'https://github.com/elastic/enterprise-search-python',
                'title': 'Elastic Enterprise Search Official Python client',
                'body': 'A descriptive body'
            }
        ]
        >>> try:
        >>>     document_results = client.index_documents(content_source_key, documents)
        >>>     print(document_results)
        >>> except EnterpriseSearchError:
        >>>     # handle exception
        >>>     pass
        [{'errors': [], 'id': '1', 'id': None}]
        """
        return self._async_create_or_update_documents(content_source_key,
                                                          documents)

    def destroy_documents(self, content_source_key, ids):
        """Destroys documents in a content source by their ids.
        Raises :class:`~elastic_enterprise_search.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises
        :class:`~elastic_enterprise_search.EnterpriseSearchError` if there are any
        HTTP errors.

        :param content_source_key: Key for the content source.
        :param ids: Array of document ids to be destroyed.
        :return: Array of result dicts, with keys of `id` and `status`

        >>> from elastic_enterprise_search import Client
        >>> from elastic_enterprise_search.exceptions import EnterpriseSearchError
        >>> content_source_key = 'content source key'
        >>> authorization_token = 'authorization token'
        >>> client = Client(authorization_token)
        >>> try:
        >>>     response = client.destroy_documents(content_source_key, ['1'])
        >>>     print(response)
        >>> except EnterpriseSearchError:
        >>>     # handle exception
        >>>     pass
        [{"id": '1',"success": True}]
        """
        endpoint = "sources/{}/documents/bulk_destroy".format(
            content_source_key)
        return self.session.request('post', endpoint, json=ids)


    def _async_create_or_update_documents(self, content_source_key, documents):
        endpoint = "sources/{}/documents/bulk_create".format(content_source_key)
        return self.session.request('post', endpoint, json=documents)
