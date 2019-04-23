Device Registration and Uninstall
=================================
Lookup, register and uninstall channels. For information about Email and SMS channels,
see their documentation.

Channel Listing
---------------

Device lists are fetched by instantiating an iterator object
using :py:class:`ChannelList`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   channel_id = None
   for channel in ua.ChannelList(airship):
       channel_id = channel.channel_id
       print (channel.channel_id, channel.device_type, channel.tags,
              channel.push_address, channel.named_user_id, channel.opt_in)

.. automodule:: urbanairship.devices.devicelist
   :members: ChannelList, ChannelInfo
   :noindex:
   :exclude-members: instance_class, from_payload

Channel Lookup
--------------

Device metadata is fetched for a specific channel by using
:py:class:`ChannelLookup:lookup`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, app_secret)

   channel = ua.ChannelInfo(airship).lookup(device_channel)
   print (channel.channel_id, channel.device_type, channel.tags,
          channel.push_address, channel.named_user_id, channel.opt_in)

.. automodule:: urbanairship.devices.devicelist
   :members: ChannelInfo
   :noindex:
   :exclude-members: from_payload

Channel Uninstall
---------------------
Channels can be uninstalled using :py:class:`ChannelUninstall`.
There is a limit of 200 channels that can be uninstalled at one time.
For more information, see:
https://docs.airship.com/api/ua/#operation/api/channels/uninstall/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    cu = ua.ChannelUninstall(airship)

    chans = [{"channel_id": "00000000-00000000-00000000-00000000",
              "device_type": "ios"},
              {"channel_id": "11111111-11111111-11111111-11111111",
              "device_type": "android"}]

    cu.uninstall(chans)

.. automodule:: urbanairship.devices.channel_uninstall

Device Listing
--------------

Device lists are fetched by instantiating an iterator object for each
type of device. The available iterators are :py:class:`DeviceTokenList` and
:py:class:`APIDList`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   for dt in ua.DeviceTokenList(airship):
      print (dt.device_token, dt.tags or [], dt.active)

   for a in ua.APIDList(airship):
      print (a.apid, a.tags or [], a.active)

.. automodule:: urbanairship.devices.devicelist
   :members: DeviceTokenList, APIDList, DeviceInfo
   :noindex:
   :exclude-members: instance_class, from_payload


Open Channel Registration
-------------------------

Open Channels are registered by using :py:class:`OpenChannel`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   my_channel = ua.OpenChannel(airship)
   my_channel.address = 'my_email@example.com'
   my_channel.open_platform = 'email'
   my_channel.opt_in = True
   my_channel.create()

   print (my_channel.channel_id, my_channel.address)

Existing channels can be updated by using the update method on
:py:class:`OpenChannel`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   my_channel = ua.OpenChannel(airship).lookup(
       '4e517ffb-af1a-4383-b0a7-e76561053749'
   )
   my_channel.tags = ['a_new_tag']
   my_channel.update(set_tags=True)

.. automodule:: urbanairship.devices.open_channel
   :members: OpenChannel
   :noindex: