import pytest


class TestPermissions:
    @pytest.mark.vcr
    def test_list_all_permissions(self, client, content_source_key):
        resp = client.permissions.list_all_permissions(content_source_key)
        assert resp == {
            "meta": {
                "page": {"current": 1, "total_pages": 1, "total_results": 1, "size": 25}
            },
            "results": [{"permissions": ["permission1"], "user": "enterprise_search"}],
        }

    @pytest.mark.vcr
    def test_list_all_permissions_with_paging(self, client, content_source_key):
        resp = client.permissions.list_all_permissions(
            content_source_key, current=2, size=20
        )
        assert resp == {
            "meta": {
                "page": {"current": 2, "total_pages": 1, "total_results": 1, "size": 20}
            },
            "results": [],
        }

    @pytest.mark.vcr
    def test_add_user_permissions(self, client, content_source_key):
        resp = client.permissions.add_user_permissions(
            content_source_key,
            user="enterprise_search",
            options={"permissions": ["permission1"]},
        )
        assert resp == {"user": "enterprise_search", "permissions": ["permission1"]}

    @pytest.mark.vcr
    def test_get_user_permissions(self, client, content_source_key):
        resp = client.permissions.get_user_permissions(
            content_source_key, user="enterprise_search"
        )
        assert resp == {"user": "enterprise_search", "permissions": ["permission1"]}

    @pytest.mark.vcr
    def test_update_user_permissions(self, client, content_source_key):
        resp = client.permissions.update_user_permissions(
            content_source_key,
            user="enterprise_search",
            options={"permissions": ["permission1", "permission2"]},
        )
        assert resp == {
            "user": "enterprise_search",
            "permissions": ["permission1", "permission2"],
        }

    @pytest.mark.vcr
    def test_remove_user_permissions(self, client, content_source_key):
        resp = client.permissions.remove_user_permissions(
            content_source_key,
            user="enterprise_search",
            options={"permissions": ["permission2"]},
        )
        assert resp == {"permissions": ["permission1"], "user": "enterprise_search"}
