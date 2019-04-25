SMS
===
Register and manage SMS channels.

Sms Channel Registration
------------------------
Begin the opt-in process for a new Sms channel.

If the `opted-in` timestamp is not included, a channel id value will not be created.
For more information see:
https://docs.airship.com/api/ua/#operation/api/channels/sms/post


.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    sms = ua.Sms(airship, sender='12345', msisdn='15035556789')

    sms.register(opted_in='2018-02-13T11:58:59')

.. automodule:: urbanairship.devices.sms
   :members: Sms
   :noindex:


SMS Channel Opt-Out
-------------------
This will mark an SMS channel as opted-out (inactive). It will not receive
alerts even when they are addressed in the future.
To opt the user back in, call the registration function again with a
valid opted_in value.

For more information, see:
https://docs.airship.com/api/ua/#operation/api/channels/sms/opt-out/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    sms = ua.Sms(airship, sender='12345', msisdn='15035556789')

    sms.opt_out()

 .. automodule:: urbanairship.devices.sms
   :members: Sms
   :noindex:


SMS Channel Uninstall
---------------------
Removes phone numbers (MSISDNs) and accompanying data from Airship.
Use with caution.

Uninstalling an SMS channel will prevent you from retrieving opt-in and
opt-out history for the corresponding MSISDN. If the uninstalled MSISDN
opts-in again, it may generate a new channel_id.

For more information, see:
https://docs.airship.com/api/ua/#operation/api/channels/sms/uninstall/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    sms = ua.Sms(airship, sender='12345', msisdn='15035556789')

    sms.uninstall()

 .. automodule:: urbanairship.devices.sms
   :members: Sms
   :noindex:


SMS Channel Lookup
------------------
Look up information on an SMS channel by `sender` and `MSISDN`.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('app_key', 'master_secret')
    sms = ua.Sms(airship, sender='12345', msisdn='15035556789')

    channel_info = sms.lookup()

 .. automodule:: urbanairship.devices.sms
   :members: Sms
   :noindex:
