Experiments
===========

With experiments endpoint you can easily manage your experiments (A/B tests) for an app.
An experiment or A/B test
is a set of distinct push notification variants sent to subsets of an audience.
You can create up to 26 notification variants and send each variant to an audience subset.
Create A/B Tests using the /api/experiments endpoint. 
<https://docs.airship.com/api/ua/#tag/a/b-tests>


Create an A/B Test
---------------------
Ceate an experiment for this application. For more information, see:
https://docs.airship.com/api/ua/#schemas%2fexperimentobject

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    audience = "all"
    ab_test = ua.AB_test(airship)
    
.. code-block:: python


Create an Experiment
---------------------

.. code-block:: python

        experiment = ua.Experiment(
        name=name,
        audience=audience,
        control=0.5,
        description=description,
        device_types=device_types,
        campaigns=campaigns,
        variants=variant_1
    )
    ab_test = ua.AB_test(airship=airship)
    r = ab_test.create(experiment=experiment)

.. code-block:: python


Create a Variant
----------------
The variants for the experiment.
An experiment must have at least 1 variant and no more than 26.
Required to have a Push object withing:
https://docs.airship.com/api/ua/#schemas%2fexperimentobject

.. code-block:: python

    push_1 = airship.create_push()
    in_app_message = ua.in_app(alert="This part appears in-app!",
                                display_type="banner",
                                expiry="2025-10-14T12:00:00",
                                display={"position": "top"},
                                actions={"add_tag": "in-app"}
                                )
    push_1.notification = ua.notification(alert="test message 1")
    push_1.in_app = in_app_message
    push_2 = airship.create_push()
    push_2.notification = ua.notification(alert="test message 2")

    variant_1 = ua.Variant(
        push_1,
        description="A description of the variant one",
        name="Testing",
        schedule={"scheduled_time": "2025-10-10T18:45:30"},
        weight=3)

.. code-block:: python


Delete Experiment
------------------------
Delete a scheduled experiment. You can only delete experiments before they start;
For more information, see:
https://docs.airship.com/api/ua/#operation/api/experiments/scheduled/experiment_id/delete

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    experiment = ua.AB_test(airship)

    experiment.delete("d9bd410d-29cf-4b17-9272-80a3f3f0662c")

.. code-block:: python


Validating an Experiment
------------------------
Parses and validates the payload without creating the experiment.
For more information, see:
https://docs.airship.com/api/ua/#operation/api/experiments/validate/post

.. code-block:: python

        import urbanairship as ua
        airship = ua.Airship("app_key", "master_secret")
        ab_test = ua.AB_test(airship=airship)
        r = ab_test.validate(experiment=experiment)

.. code-block:: python



Experiment lookup
-----------------
Look up an experiment (A/B Test). For more information see:
https://docs.airship.com/api/ua/#operation/api/experiments/experiment_id/get

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    experiment = ua.AB_test(airship)

    experiment.lookup("d9bd410d-29cf-4b17-9272-80a3f3f0662c")

.. code-block:: python
