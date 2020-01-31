class Documents:

    def __init__(self, session):
        self.session = session

    def index_documents(self, content_source_key, documents, **kwargs):
        """Index a batch of documents in a content source.
        Raises :class:`~elastic_workplace_search.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises
        :class:`~elastic_workplace_search.WorkplaceSearchError` if there are any
        HTTP errors.

        :param content_source_key: Key for the content source.
        :param documents: Array of documents to be indexed.
        :return: Array of document indexing results.

        >>> from elastic_workplace_search import Client
        >>> from elastic_workplace_search.exceptions import WorkplaceSearchError
        >>> content_source_key = 'content source key'
        >>> authorization_token = 'authorization token'
        >>> client = Client(authorization_token)
        >>> documents = [
            {
                'id': '1',
                'url': 'https://github.com/elastic/workplace-search-python',
                'title': 'Elastic Workplace Search Official Python client',
                'body': 'A descriptive body'
            }
        ]
        >>> try:
        >>>     document_results = client.documents.index_documents(content_source_key, documents)
        >>>     print(document_results)
        >>> except WorkplaceSearchError:
        >>>     # handle exception
        >>>     pass
        [{'errors': [], 'id': '1', 'id': None}]
        """
        return self._async_create_or_update_documents(content_source_key,
                                                          documents)

    def delete_documents(self, content_source_key, ids):
        """Destroys documents in a content source by their ids.
        Raises :class:`~elastic_workplace_search.NonExistentRecord` if the
        content_source_key is malformed or invalid. Raises
        :class:`~elastic_workplace_search.WorkplaceSearchError` if there are any
        HTTP errors.

        :param content_source_key: Key for the content source.
        :param ids: Array of document ids to be destroyed.
        :return: Array of result dicts, with keys of `id` and `status`

        >>> from elastic_workplace_search import Client
        >>> from elastic_workplace_search.exceptions import WorkplaceSearchError
        >>> content_source_key = 'content source key'
        >>> authorization_token = 'authorization token'
        >>> client = Client(authorization_token)
        >>> try:
        >>>     response = client.documents.delete_documents(content_source_key, ['1'])
        >>>     print(response)
        >>> except WorkplaceSearchError:
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
