=========================================
Swiftype Enterprise API Client for Python
=========================================

About
=====

A Python client for interacting with Swiftype Enterprise content sources. For
more information, go to our `generic documentation page
<https://app.swiftype.com/ent/docs/custom_sources>`_.

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
source `here <https://app.swiftype.com/ent/sources/custom/new>`:

.. code-block:: python

    >>> from swiftype_enterprise import SwiftypeEnterpriseClient
    >>> from swiftype_enterprise.exceptions import SynchronousDocumentIndexingFailed
    >>> content_source_key = 'content source key'
    >>> authorization_token = 'authorization token'
    >>> client = SwiftypeEnterpriseClient(authorization_token)
    >>> documents = [
        {
            'external_id': '1',
            'url': 'https://github.com/swiftype/swiftype-enterprise-python',
            'title': 'Swiftype Enterprise Python Github',
            'body': 'A descriptive body'
        }
    ]
    >>> try:
    >>>     document_receipt_ids = client.index_documents(content_source_key, documents, timeout=10, delay=2)
    >>>     print(document_receipt_ids)
    >>> except SynchronousDocumentIndexingFailed:
    >>>     # Timed out before documents could finish indexing
    [{'status': 'complete', 'errors': [], 'external_id': 'doc_receipt_1', 'id': '1', 'links': {'document_receipt': 'http://localhost:3002/api/v1/ent/document_receipts/5955d325f81eeace502f0a50'}}, ...]

