<p align="center"><a href="https://circleci.com/gh/elastic/workplace-search-python"><img src="https://circleci.com/gh/elastic/workplace-search-python.svg" alt="CircleCI build"></a>

> A first-party Python client for [Elastic Workplace Search](https://www.elastic.co/workplace-search).

## Contents

+ [Getting started](#getting-started-)
+ [Usage](#usage)
+ [FAQ](#faq-)
+ [Contribute](#contribute-)
+ [License](#license-)

***

## Getting started 🐣

Supports Python 2.7 and Python 3.3+.

Depends on [futures](https://github.com/PythonCharmers/python-future) and [requests](https://github.com/requests/requests).

Installed with
`pip <http://pypi.python.org/pypi/pip>`:

```bash
$ python -m pip install elastic_workplace_search
```

You can also download and install the project source:

```bash
$ python setup.py install
```

## Usage

### Creating a new Client

```python
  from elastic_workplace_search import Client
  authorization_token = 'authorization token'
  client = Client(authorization_token)
```

Retrieve your access token and a content source key after creating your content source.

### Change API endpoint

```python
client = Client(authorization_token, "https://your-server.example.com/api/ws/v1")
```

### Custom Source Documents

Document API features are found in the `client.documents` module.

#### Indexing Documents

Indexing a document into a custom content source:

```python
  content_source_key = 'content source key'
  documents = [
    {
      'id': '1234',
      'url': 'https://github.com/elastic/workplace-search-python',
      'title': 'Elastic Workplace Search Official Python Client',
      'body': 'A descriptive body, with document contents and metadata'
    }
  ]

  client.documents.index_documents(content_source_key, documents)
```

#### Deleting Documents

Deleting a document from a custom content source:

```python
  content_source_key = 'content source key'
  ids = ['1234']

  client.documents.delete_documents(content_source_key, ids)
```

### Permissions

Permissions API features are found in the `client.permissions` module.

#### Listing all permissions

```python
content_source_key = 'content source key'

client.permissions.list_all_permissions(content_source_key)
```

#### Listing all permissions with paging

```python
content_source_key = 'content source key'

client.permissions.list_all_permissions(content_source_key, size=20, current=2)
```

#### Retrieve a User's permissions

```python
content_source_key = 'content source key'
user = 'enterprise_search'

client.permissions.get_user_permissions(content_source_key, user)
```

#### Add permissions to a User

```python
content_source_key = 'content source key'
user = 'enterprise_search'
permissions = ['permission1']

client.permissions.add_user_permissions(content_source_key, 'enterprise_search', { 'permissions': permissions })
```

#### Update a User's permissions

```python
content_source_key = 'content source key'
user = 'enterprise_search'
permissions = ['permission2']

client.permissions.update_user_permissions(content_source_key, 'enterprise_search', { 'permissions': permissions })
```

#### Remove permissions from a User

```python
content_source_key = 'content source key'
user = 'enterprise_search'
permissions = ['permission2']

client.permissions.remove_user_permissions(content_source_key, 'enterprise_search', { 'permissions': permissions })
```

## FAQ 🔮

### Where do I report issues with the client?

If something is not working as expected, please open an [issue](https://github.com/elastic/workplace-search-python/issues/new).

## Contribute 🚀

We welcome contributors to the project. Before you begin, a couple notes...

+ Before opening a pull request, please create an issue to [discuss the scope of your proposal](https://github.com/elastic/workplace-search-python/issues).
+ Please write simple code and concise documentation, when appropriate.

## License 📗

[Apache 2.0](https://github.com/elastic/workplace-search-python/blob/master/LICENSE.txt) © [Elastic](https://github.com/elastic)

Thank you to all the [contributors](https://github.com/elastic/workplace-search-python/graphs/contributors)!
