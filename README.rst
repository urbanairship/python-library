About
=====

``urbanairship3`` is a Python library for using the `Urban Airship
<http://urbanairship.com/>`_ web service API for push notifications and rich
app pages. This is a fork of original ``urbanairship`` with Python 3 support.

**Why fork?** Primarily for publishing Python 3 compatible version at PyPi for easier install.

Install
=======

    pip install urbanairship3

Requirements
============

As of version 0.6, Python 2.6+ or 3.3+ is required.

Functionality
=============

Version 0.6 is a major upgrade, focusing on support for the new version 3 push
API. There has also been a major reorganization of the codebase.

* device token registration
* basic push
* registering and pushing with tags
* broadcast
* feedback service
* device token deactivation (deregistration)
* device token listing
* rich push
* scheduled notifications

Usage
=====

See the `full documentation
<http://docs.urbanairship.com/reference/libraries/python>`_, as well as the
`Urban Airship API Documentation
<http://docs.urbanairship.com/reference/api/>`_.

Simple iOS Push
---------------

    >>> import urbanairship as ua
    >>> airship = ua.Airship('application_key','master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.or_(ua.alias('adam'), ua.device_token('some_token'))
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.all_
    >>> push.send()

Broadcast to iOS, Android, and BlackBerry devices
-------------------------------------------------
    >>> push = airship.create_push()
    >>> push.audience = ua.all_
    >>> push.notification = ua.notification(
    ...     ios=ua.ios(alert='Hello iOS'),
    ...     android=ua.android(alert='Hello Android'),
    ...     blackberry=ua.blackberry(alert='Hello BlackBerry'))
    >>> push.device_types = ua.device_types('ios', 'android', 'blackberry')
    >>> push.send()

Sending a rich app page to a single iOS device
----------------------------------------------
    >>> import urbanairship as ua
    >>> airship = ua.Airship('application_key','master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.device_token('some_token')
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.device_types('ios')
    >>> push.message = ua.message(
    ...     "Hello, Rich Push User",
    ...     "<html><h1>Hello!</h1><p>Goodbye.</p></html>")
    >>> push.send()

Questions
=========

The best place to ask questions is our support site:
http://support.urbanairship.com/

History
=======

* 0.1 Initial release
* 0.2 Added tags, broadcast, feedback
* 0.3 Added deregister, device token list, other minor improvements
* 0.4 Added batch push
* 0.5 Added Android, Blackberry, Rich Push, and scheduled notifications
* 0.6 Major refactoring, support for push api v3
