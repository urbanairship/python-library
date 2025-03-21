Sending Notifications
*********************

Sending a Notification
=======================

The Airship Python Library strives to match the standard Airship API v3 JSON format
for specifying notifications. When creating a notification, you:

#. Select the audience
#. Define the notification payload
#. Specify device types
#. Deliver the notification

This example performs a broadcast with the same alert to all recipients
to a specific device type which can be a list of types:

.. code-block:: python

   import urbanairship as ua
   client = ua.client.BasicAuthClient(app_key, master_secret)

   push = ua.Push(client)
   push.audience = ua.all_
   push.notification = ua.notification(alert='Hello, world!')
   push.device_types = ua.device_types('android', 'ios')
   push.send()

Audience Selectors
------------------

An audience should specify one or more devices. An audience can be a
device, such as a ``channel``, a tag,
alias, segment, location, or a combination. Audience selectors are
combined with ``and_``, ``or_``, and ``not_``.

.. py:data:: urbanairship.push.all_

   Select all, to do a broadcast.

   .. code-block:: python

      push.audience = ua.all_


.. automodule:: urbanairship.push.audience
   :members:
   :noindex:

Notification Payload
--------------------

The notification payload determines what message and data is sent to a
device. At its simplest, it consists of a single string-valued
attribute, ``alert``, which sends a push notification consisting of a
single piece of text:

.. code-block:: python

   push.notification = ua.notification(alert='Hello, world!')

You can override the payload with platform-specific values as well:

.. code-block:: python

   push.notification = ua.notification(
       ios=ua.ios(alert='Hello iOS', badge=1),
       android=ua.android(alert='Hello Android'),
       web=ua.web(alert='Hello Web')
   )

.. automodule:: urbanairship.push.payload
   :members:
   :exclude-members: device_types

Device Types
------------

In addition to specifying the audience, you must specify the device types
you wish to target with one or more strings:

.. code-block:: python

   push.device_types = ua.device_types('ios')

.. code-block:: python

   push.device_types = ua.device_types('android', 'ios', 'web')

.. autofunction:: urbanairship.push.payload.device_types

Immediate Delivery
-------------------

Once you have set the ``audience``, ``notification``, and ``device_types``
attributes, the notification is ready for delivery. Use ``Push.send()`` to send immediately.

.. code-block:: python

   push.send()

If the request is unsuccessful, an :py:class:`AirshipFailure` exception
will be raised.

If the connection is unsuccessful, an :py:class:`ConnectionFailure` exception
will be raised.

.. autoclass:: urbanairship.push.core.Push
   :members: send, validate

Scheduled Delivery
==================

Schedule notifications for later delivery.

Examples can be found in the `documentation here. <https://docs.airship.com/api/ua/?python#tag-schedules>`_

.. autoclass:: urbanairship.push.core.ScheduledPush
   :members:
   :exclude-members: from_url, from_payload
   :noindex:

Scheduled Time Builders
-----------------------

.. autofunction:: urbanairship.push.schedule.scheduled_time
.. autofunction:: urbanairship.push.schedule.local_scheduled_time
.. autofunction:: urbanairship.push.schedule.best_time
.. autofunction:: urbanairship.push.schedule.recurring_schedule
.. autofunction:: urbanairship.push.schedule.schedule_exclusion

List Scheduled Notifications
-----------------------------

.. autoclass:: urbanairship.push.schedule.ScheduledList
   :members:
   :exclude-members: instance_class

Personalization
================
Send a notification with personalized content.

Examples can be found in `the schedules documentation here. <https://docs.airship.com/api/ua/?python#tag-personalization>`_

.. autoclass:: urbanairship.push.core.TemplatePush
   :members:

Template
--------

.. autoclass:: urbanairship.push.template.Template
   :members:
   :exclude-members: lookup, from_payload
   :noindex:

Template Lookup
---------------

.. autoclass:: urbanairship.push.template.Template
   :members: lookup
   :exclude-members: from_payload
   :noindex:

Template Listing
----------------

.. autoclass:: urbanairship.push.template.TemplateList
   :members:
   :exclude-members: instance_class

Merge Data
-----------

.. autofunction:: urbanairship.push.template.merge_data

Create and Send
================
Simultaneously send a notification to an audience of SMS, email, or open channel addresses and register channels for new addresses in your audience.

Examples can be found in `the create and send documentation here. <https://docs.airship.com/api/ua/?python#tag-create-and-send>`_

.. autoclass:: urbanairship.push.core.CreateAndSendPush
   :members:
   :noindex:

Automation
=======================

With the automation pipelines endpoint you can manage automations for
an Airship project. Pipelines define the behavior to be triggered on user-defined
events. For more information, see `the documentation on Automation
<https://docs.airship.com/api/ua/?python#tag-automation>`__.

.. autoclass:: urbanairship.automation.core.Automation
   :members:
   :noindex:

Pipeline
--------

A pipeline object encapsulates the complete set of objects that define an Automation pipeline: Triggers, Outcomes, and metadata.

.. autoclass:: urbanairship.automation.pipeline.Pipeline
   :members:
   :noindex:

A/B Tests
==========
An A/B test is a set of distinct push notification variants sent to subsets of an audience. You can create up to 26 notification variants and send each variant to an audience subset.

Examples can be found in `the A/B Tests documentation here. <https://docs.airship.com/api/ua/?python#tag-a-b-tests>`_

.. autoclass:: urbanairship.experiments.core.ABTest
   :members:
   :noindex:

Experiment
----------

.. autoclass:: urbanairship.experiments.experiment.Experiment
   :members:

Variant
-------

.. autoclass:: urbanairship.experiments.variant.Variant
   :members:
   :exclude-members: payload
