<p align="center"><img src="https://github.com/swiftype/swiftype-enterprise-python/blob/master/logo-enterprise-search.png?raw=true" alt="Elastic Enterprise Search Logo"></p>

> **⚠️ This client is deprecated ⚠️**
>
> **swiftype_enterprise has been replaced by elastic_enterprise_search. Thank you! - Elastic**

> A first-party Python client for [Elastic Enterprise Search](https://www.elastic.co/solutions/enterprise-search).

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
$ python -m pip install swiftype_enterprise
```

You can also download and install the project source:

```bash
$ python setup.py install
```

## Usage

Retrieve your access token and a content source key after creating your content source.

Indexing a document into a custom content source:

```python
  from swiftype_enterprise import SwiftypeEnterpriseClient
  content_source_key = 'content source key'
  authorization_token = 'authorization token'
  client = SwiftypeEnterpriseClient(authorization_token)
  documents = [
    {
      'id': '1234',
      'url': 'https://github.com/swiftype/swiftype-enterprise-python',
      'title': 'Swiftype Enterprise Python Github',
      'body': 'A descriptive body, with document contents and metadata'
    }
  ]

  document_results = client.index_documents(content_source_key, documents, timeout=10, delay=2)
  print(document_results)
```

### Change API endpoint

```python
client = SwiftypeEnterpriseClient(authorization_token, "https://your-server.example.com/api/v1/ent")
```

## FAQ 🔮

### Where do I report issues with the client?

If something is not working as expected, please open an [issue](https://github.com/swiftype/swiftype-enterprise-python/issues/new).

## Contribute 🚀

We welcome contributors to the project. Before you begin, a couple notes...

+ Before opening a pull request, please create an issue to [discuss the scope of your proposal](https://github.com/swiftype/swiftype-enterprise-python/issues).
+ Please write simple code and concise documentation, when appropriate.

## License 📗

[MIT](https://github.com/swiftype/swiftype-enterprise-python/blob/master/LICENSE) © [Elastic](https://github.com/elastic)

Thank you to all the [contributors](https://github.com/swiftype/swiftype-enterprise-python/graphs/contributors)!
