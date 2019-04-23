Named User
==========
A Named User is a proprietary identifier that maps customer-chosen IDs, e.g., CRM data, to Channels. 
It is useful to think of a Named User as an individual consumer who might have more than one mobile device 
registered with your Airship project.
Please see the documentation here:
https://docs.airship.com/api/ua/#tag/named-users

Named User Listing
------------------
Named User lists are fetched by instantiating an iterator object
using :py:class:`NamedUserList`.
For more information, see:
https://docs.airship.com/api/ua/#operation/api/named_users/get

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    named_user_list = ua.NamedUserList(airship)

    for n in named_user_list:
        print(n.named_user_id)

.. automodule:: urbanairship.devices.named_users
   :noindex:


Association
-----------
Associate a channel with a named user ID. For more information, see:
https://docs.airship.com/api/ua/#operation/api/named_users/associate/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')

    named_user = ua.NamedUser(airship, 'named_user_id')
    named_user.associate('channel_id', 'ios')

.. automodule:: urbanairship.devices.named_users
    :members: NamedUser
    :noindex:

.. note::
    You may only associate up to 20 channels to a Named User.
    If a channel has an assigned named user and you make an additional call to 
    associate that same channel with a new named user, the original named user 
    association will be removed and the new named user and associated data will 
    take its place. Additionally, all tags associated to the original named user 
    cannot be used to address this channel unless they are also associated with 
    the new named user.


Disassociation
--------------
Remove a channel from the list of associated channels for a named user.
For more information, see:
https://docs.airship.com/api/ua/#operation/api/named_users/disassociate/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')

    named_user = ua.NamedUser(airship, 'named_user_id')
    named_user.disassociate('channel_id', 'ios')

.. automodule:: urbanairship.devices.named_users
    :members: NamedUser
    :noindex:

Lookup
------
Look up a single named user.
For more information, see: https://docs.airship.com/api/ua/#operation/api/named_users/get

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')

    named_user = ua.NamedUser(airship, 'named_user_id')
    user = named_user.lookup()

.. automodule:: urbanairship.devices.named_users
    :members: NamedUser
    :noindex:

Tags
----
Add, remove, or set tags on a named user. For more information and notes about 
proper use of Named User Tags as well as some caveats see: 
https://docs.airship.com/api/ua/#operation/api/named_users/tags/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    named_user = ua.NamedUser(airship, 'named_user_id')

    named_user.tag(
        'tag_group_name',
        add=['tag2', 'tag3', 'tag4'],
        remove='tag1'
    )

    named_user.tag('tag_group_name', set=['tag5', 'tag6'])

.. automodule:: urbanairship.devices.named_users
    :members: NamedUser
    :noindex:

.. note::
    A single request may contain an add or remove field, both, or a single set
    field.
