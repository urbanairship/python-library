.. image:: https://travis-ci.org/urbanairship/python-library.svg?branch=master
    :target: https://travis-ci.org/urbanairship/python-library

About
=====

``urbanairship`` is a Python library for using the `Urban Airship
<http://urbanairship.com/>`_ web service API for push notifications and rich
app pages.

Requirements
============

As of version 2.0.0, Python 2.7, 3.3 or 3.4 is required.  Newer versions
of Python may also work.

Functionality
=============

Version 2.0.0 is a feature upgrade and backwards incompatible with versions
earlier than 0.8.  This release focuses on support for Web Notify and removes
support for Blackberry and MPNS.

A more detailed list of changes can be found in the CHANGELOG.

Usage
=====

See the `full documentation
<http://docs.urbanairship.com/reference/libraries/python>`_, as well as the
`Urban Airship API Documentation
<http://docs.urbanairship.com/api/>`_.

Simple iOS Push
---------------

    >>> import urbanairship as ua
    >>> airship = ua.Airship('application_key', 'master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.or_(ua.alias('adam'), ua.ios_channel('some_ios_channel'))
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.device_types('ios')
    >>> push.send()

Broadcast to iOS and Android devices
------------------------------------
    >>> push = airship.create_push()
    >>> push.audience = ua.all_
    >>> push.notification = ua.notification(
    ...     ios=ua.ios(alert='Hello iOS'),
    ...     android=ua.android(alert='Hello Android'),
    >>> push.device_types = ua.device_types('ios', 'android')
    >>> push.send()

Sending a rich app page to a single iOS device
----------------------------------------------
    >>> import urbanairship as ua
    >>> airship = ua.Airship('application_key', 'master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.ios_channel('some_ios_channel')
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.device_types('ios')
    >>> push.message = ua.message(
    ...     "Hello, Rich Push User",
    ...     "<html><h1>Hello!</h1><p>Goodbye.</p></html>")
    >>> push.send()

Web Push to a tag
-----------------

    >>> import urbanairship as ua
    >>> airship = ua.Airship('application_key', 'master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.tag('web_tag')
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.device_types('web')
    >>> push.send()

Questions
=========

The best place to ask questions is our support site:
http://support.urbanairship.com/

History
=======

* 2.0 Support for Web Notify and more iOS 10
* 1.0 Support for In-App and iOS 10
* 0.8 Support for Reports APIs
* 0.7 Support for Python 3, major refactoring
* 0.6 Major refactoring, support for push api v3
* 0.5 Added Android, Rich Push, and scheduled notifications
* 0.4 Added batch push
* 0.3 Added deregister, device token list, other minor improvements
* 0.2 Added tags, broadcast, feedback
* 0.1 Initial release
