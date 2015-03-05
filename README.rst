About
=====

``urbanairship`` is a Python library for using the `Urban Airship
<http://urbanairship.com/>`_ web service API for push notifications and rich
app pages.

Requirements
============

As of version 0.7, Python 2.6, 2.7, 3.3 or 3.4 is required.

Functionality
=============

Version 0.7 is a major upgrade and backwards incompatible with earlier
versions.  This release focuses on support for Python 3 and the new
version 3 push API. There is also a major reorganization of the codebase.

To encourage the use of our SDK, which takes care of proper channel
registration, support for device token registration has been removed.
Support for v1 endpoints has also been removed and support for:

* blackberry pin lookup,
* lookup and listing for device tokens, and
* sending to device tokens

has been moved from v1 to v3.

A more detailed list of changes can be found in the CHANGELOG.

Version 0.6.3 is a bug fix release and its updates are compatible with the .6
series. See the CHANGELOG for more information.

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
    >>> push.audience = ua.or_(ua.alias('adam'), ua.ios_channel('some_ios_channel'))
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.device_types('ios')
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
    >>> push.audience = ua.ios_channel('some_ios_channel')
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

* 0.7 Support for Python 3, major refactoring
* 0.6 Major refactoring, support for push api v3
* 0.5 Added Android, Blackberry, Rich Push, and scheduled notifications
* 0.4 Added batch push
* 0.3 Added deregister, device token list, other minor improvements
* 0.2 Added tags, broadcast, feedback
* 0.1 Initial release
