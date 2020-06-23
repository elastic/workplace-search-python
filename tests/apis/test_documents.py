import pytest
from elastic_workplace_search.exceptions import NonExistentRecord


class TestDocuments:
    @pytest.mark.vcr
    def test_index_documents(self, client, content_source_key):
        documents = [
            {"id": 1, "url": "", "title": "", "body": ""},
            {"id": "2", "url": "", "title": "", "body": ""},
        ]

        resp = client.documents.index_documents(content_source_key, documents)
        assert list(resp) == ["results"]
        assert resp["results"] == [{"errors": [], "id": "1"}, {"errors": [], "id": "2"}]

    @pytest.mark.vcr
    def test_delete_documents(self, client, content_source_key):
        resp = client.documents.delete_documents(content_source_key, [1, "2"])
        assert list(resp) == ["results"]
        assert resp["results"] == [
            {"success": True, "id": 1},
            {"success": True, "id": "2"},
        ]

    @pytest.mark.vcr
    def test_index_documents_source_not_found(self, client):
        with pytest.raises(NonExistentRecord):
            client.documents.index_documents("bad-source-key", [1, 2])

    @pytest.mark.vcr
    def test_delete_documents_source_not_found(self, client):
        with pytest.raises(NonExistentRecord):
            client.documents.delete_documents("bad-source-key", [1, 2])
