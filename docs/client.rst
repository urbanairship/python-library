Client Classes and Authentication
********************************

The Airship Python Library supports multiple authentication methods through different client classes. Each client class inherits from :py:class:`BaseClient` and provides specific authentication functionality.

Base Client
===========

.. autoclass:: urbanairship.client.BaseClient
   :members:
   :exclude-members: _request, request

Basic Authentication
===================

The :py:class:`BasicAuthClient` is used for traditional key/secret authentication. This is the same as the deprecated `Airship` client class.

.. autoclass:: urbanairship.client.BasicAuthClient
   :members:
   :exclude-members: _request, request

Example usage:

.. code-block:: python

   import urbanairship as ua
   airship = ua.client.BasicAuthClient('<app key>', '<master secret>')

   # Create and send a push notification
   push = airship.create_push()
   push.audience = ua.all_
   push.notification = ua.notification(alert='Hello, world!')
   push.device_types = ua.device_types('ios', 'android')
   push.send()

Bearer Token Authentication
=========================

The :py:class:`BearerTokenClient` is used when you have an Airship-generated bearer token. This is useful when you want to manage token refresh yourself or when using tokens from other sources.

.. autoclass:: urbanairship.client.BearerTokenClient
   :members:
   :exclude-members: _request, request

Example usage:

.. code-block:: python

   import urbanairship as ua
   airship = ua.client.BearerTokenClient('<app key>', '<bearer token>')

   # Create and send a push notification
   push = airship.create_push()
   push.audience = ua.all_
   push.notification = ua.notification(alert='Hello, world!')
   push.device_types = ua.device_types('ios', 'android')
   push.send()

OAuth2 Authentication
====================

The :py:class:`OAuthClient` handles OAuth2 authentication using JWT assertions. It automatically manages token refresh and is recommended for production use.

.. autoclass:: urbanairship.client.OAuthClient
   :members:
   :exclude-members: _request, request, _update_session_oauth_token

Example usage:

.. code-block:: python

   import urbanairship as ua

   # Initialize with OAuth credentials
   airship = ua.client.OAuthClient(
       key='<app key>',
       client_id='<client id>',
       private_key='<private key>',
       scope=['push:write', 'channels:read']  # Optional scopes
   )

   # Create and send a push notification
   push = airship.create_push()
   push.audience = ua.all_
   push.notification = ua.notification(alert='Hello, world!')
   push.device_types = ua.device_types('ios', 'android')
   push.send()

EU Data Center Support
=====================

All client classes support the EU data center through the `location` parameter:

.. code-block:: python

   # For EU data center
   eu_airship = ua.client.BasicAuthClient(
       key='<app key>',
       secret='<master secret>',
       location='eu'
   )
