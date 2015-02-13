Segments
========

Segment Listing
---------------
Segment lists are fetched by instantiating an iterator object 
using :py:class:`SegmentList`. 
For more information, see:
http://docs.urbanairship.com/api/ua.html#segments-information

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    segment_list = ua.SegmentList(airship) 

    for segment in segment_list:
        print(segment.display_name)

.. automodule:: urbanairship.devices.segment


Creating a Segment 
------------------
Create a tag for this application. For more information, see:
http://docs.urbanairship.com/api/ua.html#segment-creation

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    seg_class = ua.Segment()
    segment = seg_class.create(airship, "display name", {"tag":"Existing Tag"})


.. automodule:: urbanairship.devices.segment
    :members: Segment

Modifying a Segment
-------------------
Change the display name and criteria for a segment. For more information, see:
http://docs.urbanairship.com/api/ua.html#put--api-segments-(segment_id)

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    seg_class = ua.Segment()
    segment = seg_class.from_id(airship, "segment_id")
    segment.display_name = "New Display Name"
    segment.criteria = {'and': [{'tag': 'new_tag'}, {'not': {'tag': 'other_tag'}}]}

.. automodule:: urbanairship.devices.segment
    :members: Segment


Deleting a Segment
-------------------
A segment can be deleted by calling the delete function on the segment.
For more information, see:
http://docs.urbanairship.com/api/ua.html#delete--api-segments-(segment_id)

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    seg_class = ua.Segment()
    segment = seg_class.from_id(airship, "segment_id")
    segment.delete()

.. automodule:: urbanairship.devices.segment
    :members: Segment


Segment Lookup 
--------------
Fetch a particular segment's display name and criteria.
http://docs.urbanairship.com/api/ua.html#get--api-segments-(segment_id)

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    seg_class = ua.Segment()
    segment = seg_class.from_id(airship, "segment_id")
    segment.delete()

.. automodule:: urbanairship.devices.segment
    :members: segment
 

