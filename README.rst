.. image:: https://github.com/urbanairship/python-library/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/urbanairship/python-library/

=====

``urbanairship`` is a Python library for using the `Airship
<http://airship.com/>`_ REST API for push notifications, message
center messages, email, and SMS.

Requirements
============

Python 3.6 or higher is required. Other requirements can be found in requirements.txt.

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

Simple Push Notification
-----------------------

    >>> import urbanairship as ua
    >>> airship = ua.client.BasicAuthClient('application_key', 'master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.all_
    >>> push.notification = ua.notification(alert='Hello, world!')
    >>> push.device_types = ua.device_types('ios', 'android')
    >>> push.send()

Using OAuth2 Authentication
-------------------------
    >>> import urbanairship as ua
    >>> airship = ua.client.OAuthClient(
    ...     key='application_key',
    ...     client_id='client_id',
    ...     private_key='private_key',
    ...     scope=['push:write']
    ... )
    >>> push = airship.create_push()
    >>> push.audience = ua.all_
    >>> push.notification = ua.notification(alert='Hello, world!')
    >>> push.device_types = ua.device_types('ios', 'android')
    >>> push.send()

Sending a Message Center Message
------------------------------
    >>> import urbanairship as ua
    >>> airship = ua.client.BasicAuthClient('application_key', 'master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.ios_channel('channel_id')
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.device_types('ios')
    >>> push.message = ua.message(
    ...     'Hello, message center user',
    ...     '<html><h1>Hello!</h1><p>Goodbye.</p></html>')
    >>> push.send()

Web Push to a Tag
----------------
    >>> import urbanairship as ua
    >>> airship = ua.client.BasicAuthClient('application_key', 'master_secret')
    >>> push = airship.create_push()
    >>> push.audience = ua.tag('web_tag')
    >>> push.notification = ua.notification(alert='Hello')
    >>> push.device_types = ua.device_types('web')
    >>> push.send()

History
=======

* 7.0 Update to client classes and authentication methods
* 6.3 Support for OAuth2 Authentication. Adds new clients module and class.
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
