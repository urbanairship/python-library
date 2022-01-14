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
import. To get started, import the package, and create an
:py:class:`Airship` object representing a single Airship project.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship('<app key>', '<master secret>')

   push = airship.Push(airship=airship)
   push.audience = ua.ios_channel('074e84a2-9ed9-4eee-9ca4-cc597bfdbef3')
   push.notification = ua.notification(ios=ua.ios(alert='Hello from Python', badge=1))
   push.device_types = ua.device_types('ios')
   push.send()

The library uses `requests`_ for communication with the Airship API,
providing connection pooling and strict SSL checking. The ``Airship``
object is threadsafe, and can be instantiated once and reused in
multiple threads.

EU Base URL
-----------

When creating an instance of ``urbanairship.Airship``, an optional argument
may be added to specify use of Airship's EU data center. This is required for projects
based in our EU data center. If no location argument is passed, the US data center will be used.

.. code-block:: python

   import urbanairship as ua
   eu_airship = ua.Airship(key='<app_key>', secret='<master_secret>', location='eu')

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

As of Python 2.7, ``DeprecationWarning`` warnings are silenced by
default. To enable them, use the ``warnings`` module:

.. code-block:: python

   import warnings
   warnings.simplefilter('default')


Exceptions
==========

.. autoclass:: urbanairship.AirshipFailure

.. autoclass:: urbanairship.Unauthorized


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
