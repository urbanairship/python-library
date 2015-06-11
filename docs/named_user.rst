Named User
==========

Named User Listing
------------------
Named User lists are fetched by instantiating an iterator object
using :py:class:`NamedUserList`.
For more information, see:
http://docs.urbanairship.com/api/ua.html#listing

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    named_user_list = ua.NamedUserList(airship)

    for n in named_user_list:
        print(n.named_user_id)

.. automodule:: urbanairship.devices.named_users


Association
-----------
Associate a channel with a named user ID. For more information, see:
http://docs.urbanairship.com/api/ua.html#association

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')

    named_user = ua.NamedUser(airship, 'named_user_id')
    named_user.associate('channel_id', 'device_type')

.. automodule:: urbanairship.devices.named_users
    :members: NamedUser
.. note::
    You may only associate up to 20 channels to a Named User.

Disassociation
--------------
Remove a channel from the list of associated channels for a named user.
For more information, see:
http://docs.urbanairship.com/api/ua.html#disassociation

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')

    named_user = ua.NamedUser(airship, 'named_user_id')
    named_user.disassociate('channel_id', 'device_type')

.. automodule:: urbanairship.devices.named_users
    :members: NamedUser

Lookup
------
Look up a single named user.
For more information, see: http://docs.urbanairship.com/api/ua.html#lookup

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')

    named_user = ua.NamedUser(airship, 'named_user_id')
    user = named_user.lookup()

.. automodule:: urbanairship.devices.named_users
    :members: NamedUser


