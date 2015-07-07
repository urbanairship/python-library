*******
Reports
*******

Individual Push Response Stats
==============================
Returns detailed report information about a specific push notification.
Use the push_id, which is the identifier returned by the API that represents a
specific push message delivery.
For more information,
see: http://docs.urbanairship.com/api/ua.html#individual-push-response-statistics

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('appkey', 'master_secret')
    d = ua.reports.IndividualResponseStats(airship)
    statistics = d.get('push_id')

.. automodule:: urbanairship.reports.response_statistics
    :members: IndividualPushResponseStats


Per Push Reporting
==================
Retrieve data specific to the performance of an individual push.
For more information, see: http://docs.urbanairship.com/api/ua.html#per-push-reporting

---------------
Per Push Detail
---------------


Single Request
--------------
Get the analytics detail for a specific Push ID. For more information, see:
http://docs.urbanairship.com/api/ua.html#single-request

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('appkey', 'master_secret')
    d = ua.reports.PerPushDetail(airship)
    details = d.get_single('push_id')

.. automodule:: urbanairship.reports.per_push
    :members: PerPushDetail
    :noindex:

Batch Request
-------------
Get the analytics details for an array of Push IDs. For more information,
see: http://docs.urbanairship.com/api/ua.html#batch-request

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('appkey', 'master_secret')
    d = ua.reports.PerPushDetail(airship)
    details = d.get_batch(['push_id', 'push_id2', 'push_id3'])

.. automodule:: urbanairship.reports.per_push
    :members: PerPushDetail
    :noindex:

.. note::
    There is a maximum of 100 Push IDs per request

---------------
Per Push Series
---------------
Get the default time series data. For more information,
see: http://docs.urbanairship.com/api/ua.html#per-push-series

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('appkey', 'master_secret')
    s = ua.reports.PerPushSeries(airship)
    series = s.get('push_id')

.. automodule:: urbanairship.reports.per_push
    :members: PerPushSeries
    :noindex:

Series With Precision
---------------------
Get the series data with the specified precision. The precision can be one of
the following as strings: HOURLY, DAILY, or MONTHLY. For more information, see:
http://docs.urbanairship.com/api/ua.html#per-push-series-with-precision

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('appkey', 'master_secret')
    s = ua.reports.PerPushSeries(airship)
    series = s.get_with_precision('push_id', 'HOURLY')

.. automodule:: urbanairship.reports.per_push
    :members: PerPushSeries
    :noindex:

Series With Precision and Range
-------------------------------
Get the series data with the specified precision and range. The precision can
be one of the following as strings: HOURLY, DAILY, or MONTHLY and the start and
end date must be datetime objects. For more information, see:
http://docs.urbanairship.com/api/ua.html#per-push-series-with-precision-range

.. code-block:: python

    import urbanairship as ua
    from datetime import datetime

    airship = ua.Airship('appkey', 'master_secret')
    s = ua.reports.PerPushSeries(airship)
    date1 = datetime(2015, 12, 25)
    date2 = datetime(2015, 12, 30)
    series = s.get_with_precision_and_range('push_id', 'DAILY', date1, date2)

.. automodule:: urbanairship.reports.per_push
    :members: PerPushSeries
    :noindex:
    
Response Listing
==================
Get a listing of all pushes and basic response information in a given
timeframe by instantiating an iterator object using ResponseList. 
Start and end date times are required parameters.
For more information, see:
http://docs.urbanairship.com/api/ua.html#response-listing

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('appkey', 'master_secret')
    start_date = datetime(2015, 12, 25)
    end_date = datetime(2015, 12, 30)
    limit = 20
    response_list = ua.reports.ResponseList(airship, start_date, end_date, 
        limit, 'start_id')
    for response in response_list:
        print(response.push_uuid, response.push_time, response.push_type,
            response.direct_responses, response.sends, response.group_id)

.. automodule:: urbanairship.reports.response_statistics
    :members: ResponseListing

.. note::
    limit (optional) is the number of results desired per page.
    push_id_start (optional) specifies the id of the first response to return.
