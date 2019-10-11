from requests.status_codes import codes
from elastic_enterprise_search.client import Client

try:  # python 3.3+
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch


def mock_endpoint(
    method,
    path,
    response,
    test_request=None
):
    stubbed_response = MagicMock(status_code=codes.ok,
                                 json=lambda: response)

    expected_endpoint = '{}/{}'\
        .format(Client.ELASTIC_ENTERPRISE_SEARCH_BASE_URL, path)

    def side_effect(*args, **kwargs):
        if args[0] == method and args[1] == expected_endpoint:
            if test_request:
                test_request(kwargs)
            return stubbed_response
        raise Exception('{} {} was never called'.format(
            method.upper(), expected_endpoint))

    return {
        'target': 'requests.Session.request',
        'side_effect': side_effect
    }
