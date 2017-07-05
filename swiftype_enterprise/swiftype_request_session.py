import requests
import swiftype_enterprise
from .exceptions import InvalidCredentials, NonExistentRecord, RecordAlreadyExists, BadRequest, Forbidden


class SwiftypeRequestSession:

    def __init__(self, authorization_token, base_url):
        self.authorization_token = authorization_token
        self.base_url = base_url
        self.session = requests.Session()

        headers = {
            'Authorization': "Bearer {}".format(self.authorization_token),
            'User-Agent': "swiftype-enterprise-python/{}".format(swiftype_enterprise.__version__)
        }
        self.session.headers.update(headers)

    def raise_if_error(self, response):
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

    def request(self, http_method, endpoint, **kwargs):
        url = "{}/{}".format(self.base_url, endpoint)
        response = self.session.request(http_method, url, **kwargs)
        self.raise_if_error(response)
        return response.json()
