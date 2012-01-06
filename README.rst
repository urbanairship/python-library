About
=====

This here is a library for using the `Urban Airship
<http://urbanairship.com/>`_ web service API for iPhone and Android C2DM push notifications.

Requirements
============

Tested on Python 2.5 and 2.6 -- it'll probably work on earlier versions. If
you're using Python 2.5 or earlier, you'll need to install ``simplejson``.

Functionality
=============

As of 0.41 the library handles these parts of the API:

 * device token registration
 * APID token registration
 * basic push
 * registering and pushing with tags
 * broadcast
 * feedback service
 * device token deactivation (deregistration)
 * device token listing

iOS Usage
=========

    >>> import urbanairship
    >>> airship = urbanairship.Airship(application_key, master_secret)
    >>> airship.register('valid_token', alias='adam')
    >>> airship.push({'aps': {'alert': 'Hello'}}, aliases=['adam'],
    ...     device_tokens=['some_other_token'])

Android C2DM Usage
==================

    >>> import urbanairship
    >>> airship = urbanairship.Airship(application_key, master_secret)
    >>> airship.registerAPID('valid_token', alias='matt')
    >>> airship.push({'android': {'alert': 'Hello'}}, aliases=['matt'],
    ...     device_tokens=['some_other_token'])


Unit Tests Usage
================

 * copy keys-example.ini to keys.ini
 * edit keys.ini with your test master secret and application secret keys
 * run tests.py


Questions
=========

The best place to ask questions is our developers mailing list:
http://groups.google.com/group/urbanairship-dev

History
=======

 * 0.1  Initial release
 * 0.2  Added tags, broadcast, feedback
 * 0.3  Added deregister, device token list, other minor improvements
 * 0.4  Added Android C2DM APID support
 * 0.41 Changed httplib to requests library (merged from Benjamin Smith's fork)
