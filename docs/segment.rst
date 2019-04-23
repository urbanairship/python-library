Segments
========
Segments are portions of your audience that have arbitrary metadata (e.g. tags, location data, etc) attached.

Segment Listing
---------------
Segment lists are fetched by instantiating an iterator object 
using :py:class:`SegmentList`. 

For more information, see:
https://docs.airship.com/api/ua/#operation/api/segments/get

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    segment_list = ua.SegmentList(airship) 

    for segment in segment_list:
        print(segment.display_name)

.. automodule:: urbanairship.devices.segment
    :noindex:


Create a Segment 
------------------
Create a segment for this project. For more information, see:
https://docs.airship.com/api/ua/#operation/api/segments/post

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    segment = ua.Segment()
    segment.display_name = "Display Name"
    segment.criteria = {"tag":"Existing Tag"}
    segment.create(airship)

.. automodule:: urbanairship.devices.segment
    :members: Segment
    :noindex:

.. note::
    A segment's id is automatically set upon calling *segment.create(airship)*
    and can be accessed using *segment.id*

Update a Segment
-------------------
Change the display name and criteria for a segment. For more information, see:
https://docs.airship.com/api/ua/#operation/api/segments/segment_id/put

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    segment = ua.Segment()
    segment.from_id(airship, "segment_id")
    segment.display_name = "New Display Name"
    segment.criteria = {'and': [{'tag': 'new_tag'},
                                {'not': {'tag': 'other_tag'}}]}
    segment.update(airship)

.. automodule:: urbanairship.devices.segment
    :members: Segment
    :noindex:


Delete a Segment
------------------
A segment can be deleted by calling the delete function on the segment.
For more information, see:
https://docs.airship.com/api/ua/#operation/api/segments/segment_id/delete

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    segment = ua.Segment()
    segment.from_id(airship, "segment_id")
    segment.delete(airship)

.. automodule:: urbanairship.devices.segment
    :members: Segment
    :noindex:


Segment Lookup 
--------------
Fetch a particular segment's display name and criteria.
https://docs.airship.com/api/ua/#operation/api/segments/segment_id/get

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship("app_key", "master_secret")
    segment = ua.Segment()
    segment.from_id(airship, "segment_id")

.. automodule:: urbanairship.devices.segment
    :members: Segment
    :noindex:
