from unittest import TestCase
try:  # python 3.3+
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from .mock_endpoint import mock_endpoint
from .fixtures.add_user_permissions_response import *
from .fixtures.get_user_permissions_response import *
from .fixtures.list_all_permissions_response import *
from .fixtures.list_all_permissions_with_paging_response import *
from .fixtures.remove_user_permissions_response import *
from .fixtures.update_user_permissions_response import *
from elastic_enterprise_search.client import Client


class TestPermissions(TestCase):

    def setUp(self):
        self.client = Client('authorization_token')

    def test_list_all_permissions(self):
        content_source_key = 'key'

        def test_request(request_properties):
            actual_params = request_properties.pop('params')
            expected_params = {'page[current]': 1, 'page[size]': 25}
            self.assertEqual(actual_params, expected_params)

        mocked_endpoint = mock_endpoint(
            'get',
            'sources/{}/permissions'.format(content_source_key),
            list_all_permissions_response,
            test_request
        )

        with patch(**mocked_endpoint):
            response = self.client.permissions.list_all_permissions(
                content_source_key)
            self.assertEqual(response['results'].__len__(), 2)

    def test_list_all_permissions_with_paging(self):
        content_source_key = 'key'
        page_current = 2
        page_size = 20

        def test_request(request_properties):
            actual_params = request_properties.pop('params')
            expected_params = {
                'page[current]': page_current, 'page[size]': page_size}
            self.assertEqual(actual_params, expected_params)

        mocked_endpoint = mock_endpoint(
            'get',
            'sources/{}/permissions'.format(content_source_key),
            list_all_permissions_with_paging_response,
            test_request
        )

        with patch(**mocked_endpoint):
            response = self.client.permissions.list_all_permissions(
                content_source_key, current=page_current, size=page_size)

            self.assertEqual(response['results'].__len__(), 0)
            self.assertEqual(response['meta']['page']['current'], 2)
            self.assertEqual(response['meta']['page']['size'], 20)

    def test_add_user_permissions(self):
        content_source_key = 'key'
        permissions = ['permission1']
        user = 'enterprise_search'

        def test_request(request_properties):
            actual_json = request_properties.pop('json')
            expected_json = {
                'permissions': permissions
            }
            self.assertEqual(actual_json, expected_json)

        mocked_endpoint = mock_endpoint(
            'post',
            'sources/{}/permissions/{}/add'.format(content_source_key, user),
            add_user_permissions_response,
            test_request
        )

        with patch(**mocked_endpoint):
            response = self.client.permissions.add_user_permissions(
                content_source_key,
                user,
                {'permissions': permissions}
            )

            self.assertEqual(response['permissions'], ['permission1'])

    def test_get_user_permissions(self):
        content_source_key = 'key'
        user = 'enterprise_search'

        mocked_endpoint = mock_endpoint(
            'get',
            'sources/{}/permissions/{}'.format(content_source_key, user),
            get_user_permissions_response
        )

        with patch(**mocked_endpoint):
            response = self.client.permissions.get_user_permissions(
                content_source_key,
                user
            )
            self.assertEqual(response['permissions'], ['permission1'])

    def test_update_user_permissions(self):
        content_source_key = 'key'
        permissions = ['permission2']
        user = 'enterprise_search'

        def test_request(request_properties):
            actual_json = request_properties.pop('json')
            expected_json = {
                'permissions': permissions
            }
            self.assertEqual(actual_json, expected_json)

        mocked_endpoint = mock_endpoint(
            'post',
            'sources/{}/permissions/{}'.format(content_source_key, user),
            update_user_permissions_response,
            test_request
        )

        with patch(**mocked_endpoint):
            response = self.client.permissions.update_user_permissions(
                content_source_key,
                user,
                {'permissions': permissions}
            )

            self.assertEqual(response['permissions'], ['permission2'])

    def test_remove_user_permissions(self):
        content_source_key = 'key'
        user = 'enterprise_search'
        permissions = ['permission2']

        def test_request(request_properties):
            actual_json = request_properties.pop('json')
            expected_json = {
                'permissions': permissions
            }
            self.assertEqual(actual_json, expected_json)

        mocked_endpoint = mock_endpoint(
            'post',
            'sources/{}/permissions/{}/remove'.format(
                content_source_key, user),
            remove_user_permissions_response,
            test_request
        )

        with patch(**mocked_endpoint):
            response = self.client.permissions.remove_user_permissions(
                content_source_key,
                user,
                {'permissions': permissions}
            )
            self.assertEqual(response['permissions'], [])
