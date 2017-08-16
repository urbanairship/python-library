Locations
=========

This class allows you to search for location information in
various ways.


Name Lookup
-----------

Search for a location boundary by name. The search primarily
uses the location names, but you can also filter the results
by boundary type. See `the documentation on name lookup
<http://docs.urbanairship.com/api/ua.html#name-lookup>`__
for more information.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    l = ua.LocationFinder(airship)
    l.name_lookup('name', 'type')

.. note::

    name is a required parameter, but type is optional


Coordinates Lookup
------------------

Search for a location by latitude and longitude coordinates. Type is
an optional parameter. See `the documentation on coordinates lookup
<http://docs.urbanairship.com/api/ua.html#lat-long-lookup>`__
for more information.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    l = ua.LocationFinder(airship)
    l.coordinates_lookup('lat', 'long', 'type')

.. note::

    longitude and latitude are required parameters that must be numbers.
    Type is an optional parameter.

.. automodule:: urbanairship.devices.locationfinder


Bounding Box Lookup
-------------------

Search for location using a bounding box. See the `documentation on
bounding box lookup
<http://docs.urbanairship.com/api/ua.html#bounding-box-lookup>`__
for more information.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    l = ua.LocationFinder(airship)
    l.bounding_box_lookup('lat1', 'long1', 'lat2', 'long2', 'type')

.. note::

    lat1, long1, lat2, and long2 and are required parameters that must be numbers.
    Type is an optional parameter.


Alias Lookup
------------

Search for location by alias. See the `documentation on alias lookup
<http://docs.urbanairship.com/api/ua.html#alias-lookup>`__ for more
information.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    l = ua.LocationFinder(airship)
    l.alias_lookup('us_state=CA')

.. note::

    from_alias can either be a single alias or a list of aliases.


Polygon Lookup
--------------

Search for location by polygon id. See the `documentation on polygon lookup
<http://docs.urbanairship.com/api/ua.html#polygon-lookup>`__ for more information.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    l = ua.LocationFinder(airship)
    l.polygon_lookup('id', 'zoom')

.. note::

    polygon_id needs to be a string. Zoom is a number ranging 1-20.


Location Date Ranges
--------------------

Get the possible date ranges that can be used with location endpoints. See `the documentation
on location date ranges <http://docs.urbanairship.com/api/ua.html#location-date-ranges>`__
for more information.

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship(app_key, master_secret)
    l = ua.LocationFinder(airship)
    l.date_ranges()