Examples
========

Common setup:

.. code-block:: python

   import urbanairship as ua
   airship = ua.Airship(app_key, master_secret)


Simple broadcast to all devices
-------------------------------

.. code-block:: python

   push = airship.create_push()
   push.audience = ua.all_
   push.notification = ua.notification(alert='Hello, world!')
   push.device_types = ua.device_types('android')
   push.send()


Complex audience with platform specifics
---------------------------------------------

.. code-block:: python

   push = airship.create_push()
   push.audience = ua.and_(
      ua.tag('breakingnews'),
      ua.or_(
         ua.tag('sports'),
         ua.tag('worldnews')
      )
   )
   push.notification = ua.notification(
      ios=ua.ios(
         alert='Kim Jong-Un wins U.S. Open',
         badge='+1',
         extra={'articleid': '123456'}
      ),
      android=ua.android(
         alert='Breaking Android News! Glorious Leader Kim Jong-Un wins U.S. Open!',
         extra={'articleid': 'http://m.example.com/123456'}
      ),
      amazon=ua.amazon(
      alert='Breaking Amazon News!',
      expires_after=60,
      extra={'articleid': '12345'},
      summary='This is a short message summary',
      )
      web=ua.web(
      alert='We are in your browser!',
      title='Hello Sunshine',
      icon={
            'url': 'https://www.example.com/Sunshine_icon.png'
            },
      extra={'article_id': '67890'}
      )
   )
   push.device_types = ua.device_types('ios', 'android', 'amazon')
   push.send()


Single iOS push
---------------

.. code-block:: python

   push = airship.create_push()
   push.audience = ua.ios_channel('074e84a2-9ed9-4eee-9ca4-cc597bfdbef3')
   push.notification = ua.notification(
       ios=ua.ios(alert='Kim Jong-Un is following you on Twitter')
   )
   push.device_types = ua.device_types('ios')
   push.send()


Single iOS Rich Push with notification
--------------------------------------

.. code-block:: python

   push = airship.create_push()
   push.audience = ua.ios_channel('074e84a2-9ed9-4eee-9ca4-cc597bfdbef3')
   push.notification = ua.notification(
       ios=ua.ios(alert='Kim Jong-Un is following you on Twitter')
   )
   push.device_types = ua.device_types('ios')
   push.message = ua.message('New follower', '<h1>OMG It's Kim Jong-Un</h1>')
   push.send()


Web Push to a device with full web payload
------------------------------------------

.. code-block:: python

    push = airship.create_push()
    push.audience = ua.channel('074e84a2-9ed9-4eee-9ca4-cc597bfdbef3')
    push.notification = ua.notification(
        alert='We are in your browser now!'
        web=ua.web(
            icon={
                'url': 'https://www.example.com/Sunshine_icon.png'
            },
            title='Hello Sunshine',
            extra={'article_id': '12345'},
            time_to_live=12345,
            require_interaction=False
        )
    )
    push.device_types = ua.device_types('web')
    push.send()


Open Channels send to a device with full open channel payload
-------------------------------------------------------------

.. code-block:: python

    push = airship.create_push()
    push.audience = ua.open_channel('074e84a2-9ed9-4eee-9ca4-cc597bfdbef3')
    sms_overrides = ua.open_platform(
        alert='We are in your texts now!',
        title='See my new homepage!',
        summary='A longer summary of some content',
        media_attachment='https://example.com/cat_standing_up.jpeg',
        extra={'some_info': 'for sms only'},
        interactive=ua.interactive(
            type='ua_yes_no_foreground',
            button_actions={
                'yes': ua.actions(open_={
                    'type':'url',
                    'content':'https://www.urbanairship.com'
                    }),
                'no': ua.actions(app_defined={'foo': 'bar'})
            }
        )
    )
    push.notification = ua.notification(open_platform={'sms': sms_overrides})
    push.device_types = ua.device_types('open::sms')
    push.send()


Message Center send with extra and without notification
-------------------------------------------------------

.. code-block:: python

   push = airship.create_push()
   push.audience = ua.all_
   push.device_types = ua.device_types('ios', 'android')
   push.message = ua.message(
      title='New follower',
      body='<h1>OMG It\'s Kim Jong-Un</h1>',
      extra={'articleid': 'http://m.example.com/123456'}
   )
   push.send()


Scheduled iOS Push
------------------

.. code-block:: python

   import datetime

   sched = airship.create_scheduled_push()
   sched.schedule = ua.scheduled_time(
      datetime.datetime(2022, 10, 10, 2, 45))

   sched.push = airship.create_push()
   sched.push.audience = ua.ios_channel('074e84a2-9ed9-4eee-9ca4-cc597bfdbef3')
   sched.push.notification = ua.notification(
       ios=ua.ios(alert='Kim Jong-Un is following you on Twitter'))
   sched.push.device_types = ua.device_types('ios')

   sched.send()


In-App Message to all devices
-----------------------------

.. code-block:: python

    push = airship.create_push()
    push.audience = ua.all_
    push.device_types = ua.device_types('ios', 'android')

    push.in_app = ua.in_app(
            alert = 'Alert message',
            display_type = 'banner',
            display={
                'position': 'top',
                'duration': '500'
            },
            interactive = ua.interactive(
                type = 'ua_yes_no_foreground',
                button_actions={
                    'yes': ua.actions(open_={
                        'type':'url',
                        'content':'https://www.urbanairship.com'
                    })
                }
            )
        )
    push.send()

