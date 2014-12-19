Retrieving Device Information
=============================

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
       print channel.channel_id, channel.device_type, channel.tags,
       channel.push_address, channel.alias, channel.opt_in

.. automodule:: urbanairship.devices.devicelist
   :members: ChannelList, ChannelInfo

Channel Lookup
--------------
     
Device metadata is fetched by instantiating a lookup for a specific device
channel by using :py:class:`ChannelLookup:lookup`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, app_secret)

   channel = ua.ChannelInfo.lookup(airship, device_channel)
   print channel.channel_id, channel.device_type, channel.tags,
   channel.push_address, channel.alias, channel.opt_in

.. automodule:: urbanairship.devices.devicelist
   :members: ChannelInfo

Device Listing
--------------

Device lists are fetched by instantiating an iterator object for each type of
device. The available iterators are :py:class:`DeviceTokenList`,
:py:class:`APIDList`, and :py:class:`DevicePINList`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   for dt in ua.DeviceTokenList(airship):
      print dt.device_token, dt.tags or [], dt.active

.. automodule:: urbanairship.devices.devicelist
   :members: DeviceTokenList, DevicePINList, APIDList, DeviceInfo
