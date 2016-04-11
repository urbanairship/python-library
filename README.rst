
About
=====

``wallet`` is a Python library for using the `Urban Airship
<http://urbanairship.com/>`_ a web service API for managing Apple Wallet and Android Pay objects.

Requirements
============

Python 2.X. and Requests 2.7 or higher

Installation
============

python setup.py install

Functionality
=============

The API provides an easy to use client abstraction layer for the Urban Airship Wallet API.

http://docs.urbanairship.com/api/wallet.html

Usage
=====

For quick start please see the examples/ directory

After installation

The base Wallet object is used to access most API functions.

There are two different levels of the API:

The low level member functions on the Wallet object where the payload accepts JSON strings, dictionaries
and high level objects and directly calls the Wallet RESTful API. This requires the user to be familiar with the JSON
specification of the various endpoints in order to get the desired result.

Example: ``w.create_project( payload )``

The high level API allows you to create the various wallet primitives such as Project, Template, Field and other types
and enables simple aggregation of these objects and their internal members such as allowing fields to be added to
passes and simple function based modification of their properties.

Example: ``template = Template('My Event Ticket',TemplateType.EVENT_TICKET, project.id, Vendor.APPLE, 'Description')``

It is recommended using the high level API if possible since this will significantly reduce the complexity of the
client side code. The high level primitives are implemented using the lower level ones and feel free to dig into
the source code to gain a better understanding of the inner workings of the API.

To get started run and read the examples.

.. include:: ../examples/

Support
======

For support of the API and the client side implementation please contact:
http://support.urbanairship.com/

History
=======

* 0.2 First public release