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
       print (channel.channel_id, channel.device_type, channel.tags,
              channel.push_address, channel.alias, channel.opt_in)

.. automodule:: urbanairship.devices.devicelist
   :members: ChannelList, ChannelInfo
   :noindex:

Channel Lookup
--------------

Device metadata is fetched for a specific channel by using
:py:class:`ChannelLookup:lookup`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, app_secret)

   channel = ua.ChannelInfo.lookup(airship, device_channel)
   print (channel.channel_id, channel.device_type, channel.tags,
          channel.push_address, channel.alias, channel.opt_in)

.. automodule:: urbanairship.devices.devicelist
   :members: ChannelInfo
   :noindex:


Device Listing
--------------

Device lists are fetched by instantiating an iterator object for each
type of device. The available iterators are :py:class:`DeviceTokenList` and :py:class:`APIDList`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

   for dt in ua.DeviceTokenList(airship):
      print (dt.device_token, dt.tags or [], dt.active)

.. automodule:: urbanairship.devices.devicelist
   :members: DeviceTokenList, APIDList, DeviceInfo
   :noindex:


Open Channel Registration
--------------

Open Channels are registered by using :py:class:`OpenChannel`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, app_secret)

   my_channel = ua.OpenChannel()
   my_channel.address = 'my_email@example.com'
   my_channel.open_platform = 'email'
   my_channel.opt_in = True
   my_channel.create(airship)

   print (my_channel.channel_id, my_channel.address, my_channel.created)

Existing channels can be updated by using the update method on
:py:class:`OpenChannel`.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, app_secret)

   my_channel = ua.OpenChannel.from_id('4e517ffb-af1a-4383-b0a7-e76561053749')
   my_channel.tags = ['a_new_tag']
   my_channel.update(airship, set_tags=True)

.. automodule:: urbanairship.devices.open_channel
   :members: OpenChannel
   :noindex:


Feedback
--------
Feedback returns a list of dictionaries of device tokens/APIDs that the
respective push provider has told us are uninstalled since the given
timestamp. For more information, see: `the documentation on feedback
<feedback>`_.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   since = datetime.datetime.utcnow() - datetime.timedelta(days=1)
   tokens = ua.Feedback.device_token(airship, since)
   apids = ua.Feedback.apid(airship, since)

.. automodule:: urbanairship.devices.devicelist
   :members: Feedback
   :noindex:

.. _feedback: http://docs.urbanairship.com/api/ua.html#feedback
