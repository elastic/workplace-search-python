=========================================
Swiftype Enterprise API Client for Python
=========================================

About
=====

A Python client for interacting with Swiftype Enterprise content sources.
Documentation for this API client can be found at Readthedocs
(http://swiftype-enterprise.readthedocs.io/en/latest/). 

For more information, go to our official documentation page
(https://app.swiftype.com/ent/docs/custom_sources).

Installation
============
Swiftype Enterprise Client can be installed with
`pip <http://pypi.python.org/pypi/pip>`_::

    $ python -m pip install swiftype_enterprise

You can also download the project source and do::

    $ python setup.py install

Dependencies
============
Swiftype Enterprise Client supports Python 2.7 and Python 3.3+. It depends
on futures and requests.

Examples
========
Here's a basic example for indexing a document into a custom content source.
You can get an access token and a content source key after creating a content
source here: https://app.swiftype.com/ent/sources/custom/new

.. code-block:: python

  from swiftype_enterprise import SwiftypeEnterpriseClient
  from swiftype_enterprise.exceptions import SynchronousDocumentIndexingFailed
  content_source_key = 'content source key'
  authorization_token = 'authorization token'
  client = SwiftypeEnterpriseClient(authorization_token)
  documents = [
    {
      'external_id': '1234',
      'url': 'https://github.com/swiftype/swiftype-enterprise-python',
      'title': 'Swiftype Enterprise Python Github',
      'body': 'A descriptive body, with document contents and metadata'
    }
  ]
  try:
    document_receipts = client.index_documents(content_source_key, documents, timeout=10, delay=2)
    print(document_receipts)
  except SynchronousDocumentIndexingFailed:
    # Timed out before documents could finish indexing
    pass

