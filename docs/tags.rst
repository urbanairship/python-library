Tags
=============================

Tag Listing
-----------
Feedback returns a list of dictionaries of device tokens/APIDs that the respective
push provider has told us are uninstalled since the given timestamp. For more
information, see: http://docs.urbanairship.com/api/ua.html#feedback .

Note:
    If you'd like to parse the result, you'll need dateutil:
    http://labix.org/python-dateutil

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   since  = datetime.datetime.utcnow() - datetime.timedelta(days=1)
   tokens = airship.Feedback.device_token(airship, since)
   apids  = airship.Feedback.apid(airship, since)

.. automodule:: urbanairship.devices.devicelist
   :members: Feedback


Adding and Removing Devices from a Tag
--------------------------------------
Feedback returns a list of dictionaries of device tokens/APIDs that the respective
push provider has told us are uninstalled since the given timestamp. For more
information, see: http://docs.urbanairship.com/api/ua.html#feedback .

Note:
    If you'd like to parse the result, you'll need dateutil:
    http://labix.org/python-dateutil

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   since  = datetime.datetime.utcnow() - datetime.timedelta(days=1)
   tokens = airship.Feedback.device_token(airship, since)
   apids  = airship.Feedback.apid(airship, since)

.. automodule:: urbanairship.devices.devicelist
   :members: Feedback


Deleting a Tag
--------------
Feedback returns a list of dictionaries of device tokens/APIDs that the respective
push provider has told us are uninstalled since the given timestamp. For more
information, see: http://docs.urbanairship.com/api/ua.html#feedback .

Note:
    If you'd like to parse the result, you'll need dateutil:
    http://labix.org/python-dateutil

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   since  = datetime.datetime.utcnow() - datetime.timedelta(days=1)
   tokens = airship.Feedback.device_token(airship, since)
   apids  = airship.Feedback.apid(airship, since)

.. automodule:: urbanairship.devices.devicelist
   :members: Feedback


Batch Modification of Tags
--------------------------
Feedback returns a list of dictionaries of device tokens/APIDs that the respective
push provider has told us are uninstalled since the given timestamp. For more
information, see: http://docs.urbanairship.com/api/ua.html#feedback .

Note:
    If you'd like to parse the result, you'll need dateutil:
    http://labix.org/python-dateutil

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)
   since  = datetime.datetime.utcnow() - datetime.timedelta(days=1)
   tokens = airship.Feedback.device_token(airship, since)
   apids  = airship.Feedback.apid(airship, since)

.. automodule:: urbanairship.devices.devicelist
   :members: Feedback


