Automation
==========

With the automation pipelines endpoint you can easily manage automations for
an app. Automations define the push behavior to be triggered on user-defined
events. For more information, see `the documentation on Automations
<https://docs.urbanairship.com/api/ua/#automation-api>`__

Creating an Automation
----------------------
Create an automation for this application. For more information, see:
https://docs.urbanairship.com/api/ua/#pipelines-api
Automations are defined by one or more Pipeline objects

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    automation = ua.Automation(airship)
    pipeline = ua.Pipeline(
        airship,
        enabled=True,
        name="Automated Pipeline",
        outcome={
           "immediate_trigger": {
              "tag_added": "interests::kitchen_sinks"
           },
           "timing": {
              "delay": { "seconds": 259200 }
           },
           "cancellation_trigger": {
              "custom_event": {
                 "name": "COMPLETED_CHECKOUT"
              }
           },
           "outcome": {
              "push": {
                 "audience": "triggered",
                 "device_types": "all",
                 "notification": {
                    "alert": "Like sinks? You'll love this deal!"
                 }
              }
           }
        }
    )

    automation.create(pipeline.payload)

.. autoclass:: urbanairship.automation.core.Automation


Validating an Automation
------------------------
Validate an automation payload prior to making requests to create update.
For more information, see:
https://docs.urbanairship.com/api/ua/#post-api-pipelines-validate

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    automation = ua.Automation(airship)
    pipeline = ua.Pipeline(
        airship,
        enabled=True,
        name="Automated Pipeline",
        outcome={
           "immediate_trigger": {
              "tag_added": "interests::kitchen_sinks"
           },
           "timing": {
              "delay": { "seconds": 259200 }
           },
           "cancellation_trigger": {
              "custom_event": {
                 "name": "COMPLETED_CHECKOUT"
              }
           },
           "outcome": {
              "push": {
                 "audience": "triggered",
                 "device_types": "all",
                 "notification": {
                    "alert": "Like sinks? You'll love this deal!"
                 }
              }
           }
        }
    )

    automation.validate(pipeline.payload)

.. autoclass:: urbanairship.automation.core.Automation

.. note::
    Validating an Automation acts as a dry run and will not attempt to modify
    any information on this application.


Updating an Automation
----------------------
Update an automation with a full automation object. For more information, see:
https://docs.urbanairship.com/api/ua/#put-api-pipelines-id

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    automation = ua.Automation(airship)
    pipeline = ua.Pipeline(
        airship,
        enabled=True,
        name="Updated Pipeline",
        outcome={
           "immediate_trigger": {
              "tag_added": "interests::bathroom_sinks"
           },
           "timing": {
              "delay": { "seconds": 259200 }
           },
           "cancellation_trigger": {
              "custom_event": {
                 "name": "COMPLETED_CHECKOUT"
              }
           },
           "outcome": {
              "push": {
                 "audience": "triggered",
                 "device_types": "all",
                 "notification": {
                    "alert": "Bathroom sink issues? You'll love this deal!"
                 }
              }
           }
        }
    )

    automation.update("21bc19f7-dfcc-4a80-9d8b-6bfd350fe87b", pipeline.payload)

.. autoclass:: urbanairship.automation.core.Automation


Lookup an Automation
--------------------
Lookup an existing automation for this app. For more information, see:
https://docs.urbanairship.com/api/ua/#get-api-pipelines-id

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    automation = ua.Automation(airship)

    automation.lookup("21bc19f7-dfcc-4a80-9d8b-6bfd350fe87b")

.. autoclass:: urbanairship.automation.core.Automation


Deleting an Automation
----------------------
Delete an existing automation for this app. For more information, see:
https://docs.urbanairship.com/api/ua/#delete-api-pipelines-id

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    automation = ua.Automation(airship)

    automation.delete("21bc19f7-dfcc-4a80-9d8b-6bfd350fe87b")

.. autoclass:: urbanairship.automation.core.Automation


Automation Listing
------------------
List existing automations for this app. For more information, see:
https://docs.urbanairship.com/api/ua/#get-api-pipelines

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    automation = ua.Automation(airship)

    automation.list_automations(limit=10, enabled=True)

.. autoclass:: urbanairship.automation.core.Automation


Deleted Automation Listing
--------------------------
List deleted automations for this app. For more information, see:
https://docs.urbanairship.com/api/ua/#get-api-pipelines

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    automation = ua.Automation(airship)

    automation.list_deleted_automations(start="2015-02-14T19:19:19")

.. autoclass:: urbanairship.automation.core.Automation
