Email
=====
Register email channels, set opt-in status, and manipulate tags on email channels.
Email channels have unique properties for opt-in, tags and uninstall.
For more information, please see the API documentation: https://docs.airship.com/api/ua/#tag/email

Email Channel Registration
--------------------------
Create a new email channel or unsubscribe an existing email channel
from receiving commercial emails. To unsubscribe an existing channel,
set email_opt_in_level to `none`.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    email = ua.Email(airship=airship,
                     address='example@email.xyz',
                     opt_in_level='transactional',
                     timezone='America/Los_Angeles',
                     locale_country='US',
                     locale_language='en')
    email.register()

.. automodule:: urbanairship.devices.email
   :members: Email
   :noindex:


Uninstall Email Channel
-----------------------
Removes an email address from Urban Airship. Use with caution.
If the uninstalled email address opts-in again, it will generate a new
channel_id. The new channel_id cannot be reassociated with any opt-in
information, tags, named users, insight reports, or other information
from the uninstalled email channel.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    email = ua.Email(airship=airship,
                     address='example@email.xyz',
                     opt_in_level='transactional',
                     timezone='America/Los_Angeles',
                     locale_country='US',
                     locale_language='en')
    email.uninstall()



Add, Remove or Set Email Tags
-----------------------------
Add, remove, or set tags on one email channel.
A single request body may contain an add or remove field,
or both, or a single set field. One or more of the add, remove,
or set keys must be present.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')

    # replaces all existing tags on an email channel
    email_tags = ua.EmailTags(airship=airship,
                              address='example.email.xyz')
    email_tags.set(group='my_tag_group',
                   tags=['one', 'two', 'three'])
    email_tags.send()

    # adds and removes tags from an email channel
    email_tags = ua.EmailTags(airship=airship,
                              address='example.email.xyz')
    email_tags.remove(group='my_tag_group',
                      tags=['one', 'two', 'three'])
    email_tags.add(group='my_tag_group',
                   tags=['some', 'new', 'tags'])
    email_tags.send()