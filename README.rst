.. image:: https://github.com/urbanairship/python-library/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/urbanairship/python-library/

=====

``urbanairship`` is a Python library for using the `Airship
<http://airship.com/>`_ REST API for push notifications, message
center messages, email, and SMS.

Requirements
============

Python 2.7, 3.6, 3.7, 3.8, or 3.9 is required. Other requirements can be found in requirements.txt.

Questions
=========

The best place to ask questions or report a problem is our support site:
http://support.airship.com/

Usage
=====

See the `full documentation for this library
<https://docs.airship.com/api/libraries/python/>`_, as well as the
`Airship API Documentation
<https://docs.airship.com/api/ua/>`_.

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
    ...     android=ua.android(alert='Hello Android'))
    >>> push.device_types = ua.device_types('ios', 'android')
    >>> push.send()

Sending a message center message to a single iOS device
--------------------------------------------------------
    >>> import urbanairship as ua
    >>> airship = ua.Airship('application_key', 'master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.ios_channel('some_ios_channel')
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.device_types('ios')
    >>> push.message = ua.message(
    ...     'Hello, message center user',
    ...     '<html><h1>Hello!</h1><p>Goodbye.</p></html>')
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

History
=======

* 6.0 Support for Bearer Token Authentication. Removes support for Python 2.
* 5.0 Support for SMS and Email messages. See changelog for other updates.
* 4.0 Support for Automation, removed Feedback
* 3.0 Support for Open Channels, several other significant changes
* 2.0 Support for Web Notify and more iOS 10, stopped supporting Python 2.6
* 1.0 Support for In-App and iOS 10
* 0.8 Support for Reports APIs
* 0.7 Support for Python 3, major refactoring
* 0.6 Major refactoring, support for push api v3
* 0.5 Added Android, Rich Push, and scheduled notifications
* 0.4 Added batch push
* 0.3 Added deregister, device token list, other minor improvements
* 0.2 Added tags, broadcast, feedback
* 0.1 Initial release

See the CHANGELOG file for more details.
