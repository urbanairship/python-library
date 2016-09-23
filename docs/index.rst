##################################
Urban Airship Reach Python Library
##################################


************
Installation
************

You can install the library via ``pip``::

   $ pip install urbanairship_reach


*******
Logging
*******

``reach`` uses the standard logging module for integration into
an application's existing logging. If you do not have logging
configured otherwise, your application can set it up like so:

.. code-block:: python

   import logging
   logging.basicConfig()

If you're having trouble with the Reach API, you can turn on verbose debug
logging.

.. code-block:: python

   logging.getLogger('urbanairship').setLevel(logging.DEBUG)

As of Python 2.7, ``DeprecationWarning`` warnings are silenced by default. To
enable them, use the ``warnings`` module:

.. code-block:: python

   import warnings
   warnings.simplefilter('default')


***********
Development
***********

The library source code is `available on GitHub <github>`_. Please feel free
to submit a pull request.

Tests can be run with nose:

.. code-block:: sh

   $ nosetests


********
Contents
********

API Reference
=============

.. toctree::
   :maxdepth: 2

   templates
   passes


Walkthroughs
============

.. toctree::
   :maxdepth: 2

   creating-templates

.. _github: https://github.com/urbanairship/reach-python-library
