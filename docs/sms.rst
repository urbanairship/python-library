Sms
===

Sms Channel Registration
------------------------
Begin the opt-in process for a new Sms channel.

If the `opted-in` timestamp is not included, a channel id value will not be created.
For more information see:
https://docs.urbanairship.com/api/ua/#operation/api/channels/sms/post


.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    sms = ua.Sms(airship, sender='12345', msisdn='15035556789')

    sms.register(opted_in='2018-02-13T11:58:59')

.. automodule:: urbanairship.devices.sms
   :members: Sms
   :noindex:


Sms Channel Opt-Out
-------------------
This will mark an Sms channel as opted-out (inactive) and it will not receive
alerts even when they are addressed in the future.
To opt the user back in, call the registration function again with a
valid opted_in value.

For more information, see:
https://docs.urbanairship.com/api/ua/#operation/api/channels/sms/opt-out/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    sms = ua.Sms(airship, sender='12345', msisdn='15035556789')

    sms.opt_out()

 .. automodule:: urbanairship.devices.sms
   :members: Sms
   :noindex:


Sms Channel Uninstall
---------------------
Removes phone numbers and accompanying data from Urban Airship.
Use with caution.

Uninstalling an Sms channel will prevent you from retrieving opt-in and
opt-out history for the corresponding msisdn. If the uninstalled msisdn
opts-in again, it will generate a new channel_id.

For more information, see:
https://docs.urbanairship.com/api/ua/#operation/api/channels/sms/uninstall/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    sms = ua.Sms(airship, sender='12345', msisdn='15035556789')

    sms.uninstall()

 .. automodule:: urbanairship.devices.sms
   :members: Sms
   :noindex:


Sms Channel Lookup
------------------
Look up information on an Sms channel by `sender` and `MSISDN`.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    sms = ua.Sms(airship, sender='12345', msisdn='15035556789')

    channel_info = sms.lookup()

 .. automodule:: urbanairship.devices.sms
   :members: Sms
   :noindex:
