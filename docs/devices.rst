Retrieving Device Information
=============================

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
