Tags
====

A note about using the tag API: if using UrbanAirship SDKs, it is not advisable
to use the tag API unless you have device-side tagging disabled in the SDK. Without 
this setting disabled, the modifications made using the tag API will be overwritten by settings in the SDK.


Tag Listing
-----------
Lists tags that exist for this application. Tag Listing will return 
up to the first 100 tags per application.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   list_tags = ua.TagList(airship)
   list_tags.listTags()

.. automodule:: urbanairship.devices.tag
   :members: TagList


Adding Devices to a Tag
--------------------------------------
Add one or more channels to a particular tag. For more
information, see: 
http://docs.urbanairship.com/api/ua.html#adding-and-removing-devices-from-a-tag .

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   devices = ua.Tag(airship, "working_tag")
   devices.add(ios_channels=['ios_channel_id'], 
               android_channels=['android_channel_id', 'android_channel_id_2'])

.. automodule:: urbanairship.devices.tag
   :members: Tag


Removing Devices from a Tag
--------------------------------------
Remove one or more channels from a particular tag. For more
information, see: 
http://docs.urbanairship.com/api/ua.html#adding-and-removing-devices-from-a-tag .

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   devices = ua.Tag(airship, "working_tag")
   devices.remove(ios_channels=['ios_channel_id'], 
               android_channels=['android_channel_id', 'android_channel_id_2'])

.. automodule:: urbanairship.devices.tag
   :members: Tag

Deleting a Tag
--------------
A tag can be removed from our system by issuing a delete. This will remove the
master record of the tag. For more information, see: 
http://docs.urbanairship.com/api/ua.html#deleting-a-tag .

Note:
    Delete will remove the tag from all devices with the exception of devices that 
    are inactive due to uninstall. Devices that were uninstalled will retain their tags.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   delete_tag = ua.DeleteTag(airship, "tag_to_delete")
   delete_tag.send_delete()

.. automodule:: urbanairship.devices.tag
   :members: DeleteTag


Batch Modification of Tags
--------------------------
Modify the tags for a number of device channels. For more
information, see: http://docs.urbanairship.com/api/ua.html#batch-modification-of-tags .

Note:
    You must include an object containing an ios_channel, android_channel, or
    amazon_channel, and a list of tags to apply.

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   send_batch = ua.BatchTag(airship)
   send_batch.addIOSChannel('ios_channel_id', ['ios_tag', 'portland_OR'])
   send_batch.addAndroidChannel('android_channel_id', ['tag11', 'tag12'])
   send_batch.addAmazonChannel('amazon_channel_id', ['tag11', 'portland_OR'])
   send_batch.send_request()

.. automodule:: urbanairship.devices.tag
   :members: BatchTag


