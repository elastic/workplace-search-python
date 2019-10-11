
# Implements the Document Permissions API:
#  https://swiftype.com/documentation/enterprise-search/api/document-permissions


class Permissions:

    def __init__(self, session):
        self.session = session

    def list_all_permissions(self, content_source_key, current=1, size=25):
        endpoint = 'sources/{}/permissions'.format(content_source_key)
        params = {'page[current]': current, 'page[size]': size}
        return self.session.request('get', endpoint, params=params)

    def get_user_permissions(self, content_source_key, user):
        endpoint = 'sources/{}/permissions/{}'.format(content_source_key, user)
        return self.session.request('get', endpoint)

    def update_user_permissions(self, content_source_key, user, options):
        endpoint = 'sources/{}/permissions/{}'.format(content_source_key, user)
        return self.session.request('post', endpoint, json=options)

    def add_user_permissions(self, content_source_key, user, options):
        endpoint = 'sources/{}/permissions/{}/add'.format(
            content_source_key, user)
        return self.session.request('post', endpoint, json=options)

    def remove_user_permissions(self, content_source_key, user, options):
        endpoint = 'sources/{}/permissions/{}/remove'.format(
            content_source_key, user)
        return self.session.request('post', endpoint, json=options)
