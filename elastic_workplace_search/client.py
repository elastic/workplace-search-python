from .request_session import RequestSession
from .apis.documents import Documents
from .apis.permissions import Permissions

"""API client for Elastic Enterprise Search"""


class Client:

    ELASTIC_ENTERPRISE_SEARCH_BASE_URL = 'http://localhost:3002/api/v1/ent'

    def __init__(self, authorization_token, base_url=ELASTIC_ENTERPRISE_SEARCH_BASE_URL):
        self.authorization_token = authorization_token
        self.base_url = base_url
        self.session = RequestSession(self.authorization_token, self.base_url)

        self.documents = Documents(self.session)
        self.permissions = Permissions(self.session)
