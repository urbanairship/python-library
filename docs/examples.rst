Examples
========

Common setup:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)

Simple broadcast to all devices
-------------------------------

.. code-block:: python

   push = ua.create_push()
   push.audience = ua.all_
   push.notification = ua.notification(alert="Hello, world!")
   push.device_types = ua.all_
   push.send()


Complex audience with iOS & Android specifics
---------------------------------------------

.. code-block:: python

   push = ua.create_push()
   push.audience = ua.and_(
      ua.tag("breakingnews"),
      ua.or_(
         ua.tag("sports"),
         ua.tag("worldnews")
      )
   )
   push.notification = ua.notification(
      ios=ua.ios(
         alert="Kim Jong-Un wins U.S. Open",
         badge="+1",
         extra={"articleid": "123456"}
      ),
      android=ua.android(
         alert="Breaking Special Android News! Glorious Leader Kim Jong-Un wins U.S. Open!",
         extra={"articleid": "http://m.example.com/123456"}
      )
   )
   push.device_types = ua.device_types('ios', 'android')
   push.send()


Single iOS push
---------------

.. code-block:: python

   push = ua.create_push()
   push.audience = ua.device_token('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
   push.notification = ua.notification(
       ios=ua.ios(alert="Kim Jong-Un is following you on Twitter"))
   push.device_types = ua.device_types('ios')
   push.send()

Single iOS Rich Push
--------------------

.. code-block:: python

   push = ua.create_push()
   push.audience = ua.device_token('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
   push.notification = ua.notification(
       ios=ua.ios(alert="Kim Jong-Un is following you on Twitter"))
   push.device_types = ua.device_types('ios')
   push.message = ua.message("New follower", "<h1>OMG It's Kim Jong-Un</h1>")
   push.send()

Sheduled iOS Push
-----------------

.. code-block:: python

   sched = ua.create_scheduled_push()
   sched.schedule = ua.scheduled_time("2013-10-10T02:45:00")

   seched.push = ua.create_push()
   sched.push.audience = ua.device_token('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
   sched.push.notification = ua.notification(
       ios=ua.ios(alert="Kim Jong-Un is following you on Twitter"))
   sched.push.device_types = ua.device_types('ios')

   sched.send()
