Airship Python Library
***********************

``urbanairship`` is a Python library for using the `Airship
<http://airship.com/>`_ web service in support of our messaging product
lines and related features.

Installation
=============

Using ``pip``::

   $ pip install urbanairship

Using the library
==================

The library is intended to be used with the small footprint of a single
import. To get started, import the package, and create an appropriate client object
representing a single Airship project.

.. code-block:: python

   import urbanairship as ua
   airship = ua.client.BasicAuthClient('<app key>', '<master secret>')

   push = airship.create_push()
   push.audience = ua.all_
   push.notification = ua.notification(alert='Hello, world!')
   push.device_types = ua.device_types('ios', 'android')
   push.send()

The library uses `requests`_ for communication with the Airship API,
providing connection pooling and strict SSL checking. All client objects are
threadsafe, and can be instantiated once and reused in multiple threads.

Authentication
-------------

The library supports three authentication methods:

* Basic Authentication - Using app key and master secret
* Bearer Token Authentication - Using app key and Airship-generated bearer token
* OAuth2 Authentication - Using JWT assertions with automatic token refresh

For more details on each authentication method, see the :doc:`client` documentation.

Logging
-------

``urbanairship`` uses the standard logging module for integration into
an application's existing logging. If you do not have logging
configured otherwise, your application can set it up like so:

.. code-block:: python

   import logging
   logging.basicConfig()

If you're having trouble with the Airship API, you can turn on verbose debug
logging.

.. code-block:: python

   logging.getLogger('urbanairship').setLevel(logging.DEBUG)

Exceptions
==========

.. autoclass:: urbanairship.AirshipFailure

.. autoclass:: urbanairship.Unauthorized

.. autoclass:: urbanairship.ConnectionFailure

Development
============

The library source code is `available on GitHub <github>`_.

Tests can be run with nose_:

.. code-block:: sh

   nosetests --with-doctest

Contents
=========

.. toctree::
   :maxdepth: 3

   client
   push.rst
   devices.rst
   audience.rst
   reports.rst
   custom_events.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _channels: https://docs.airship.com/api/ua/?python#tag-channels
.. _requests: http://python-requests.org
.. _github: https://github.com/urbanairship/python-library
.. _nose: https://nose.readthedocs.org/en/latest/
