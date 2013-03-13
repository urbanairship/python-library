About
=====

This here is a library for using the `Urban Airship
<http://urbanairship.com/>`_ web service API for iPhone push notifications.

Requirements
============

Tested on Python 2.5 and 2.6 -- it'll probably work on earlier versions. If
you're using Python 2.5 or earlier, you'll need to install ``simplejson``.

Functionality
=============

As of 0.5 the library handles these parts of the API:

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

Simple iOS Push
---------------
    >>> import urbanairship
    >>> airship = urbanairship.Airship(application_key, master_secret)
    >>> airship.push({'aps': {'alert': 'Hello'}}, aliases=['adam'],
    ...     device_tokens=['some_other_token'])

Broadcast to iOS, Android, and BlackBerry devices
-------------------------------------------------
    >>> import urbanairship
    >>> airship = urbanairship.Airship(application_key, master_secret)
    >>> airship.broadcast({
    ...     'aps': {'alert': 'Hello iOS'},
    ...     'android': {'alert': 'Hello Android'},
    ...     'blackberry': {
    ...         'body': 'Hello BlackBerry',
    ...         'content-type': 'text/plain',
    ...     },
    ... })

Sending a Rich Push message to a single user
--------------------------------------------
    >>> import urbanairship
    >>> airship = urbanairship.Airship(application_key, master_secret)
    >>> richpush = airship.create_rich_push()
    >>> richpush.add_recipents(users=["<user_id>"])
    >>> richpush.set_message(
    ...     "Hello, Rich Push User",
    ...     "<html><h1>Hello!</h1><p>Goodbye.</p></html>")
    >>> richpush.send()

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
* 0.6 Added Android APID Tagging and Aliasing
