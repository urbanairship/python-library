*******
Reports
*******

Individual Push Response Stats
==============================

Returns detailed report information about a specific push notification.
Use the push_id, which is the identifier returned by the API that represents a
specific push message delivery.
For more information,
see `the documentation on Individual Push Response Stats
<http://docs.urbanairship.com/api/ua.html#individual-push-response-statistics>`_

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('appkey', 'master_secret')
    d = ua.reports.IndividualResponseStats(airship)
    statistics = d.get('push_id')


Devices Report
==============

Returns an app’s opted-in and installed device counts broken out by device
type. This endpoint returns the same data that populates the Devices Report.
For more information, see `the documentation on the Devices Report
<http://docs.urbanairship.com/api/ua.html#devices-report-api>`_

.. code-block:: python

    import urbanairship as ua
    airship = ua.Airship('appkey', 'master_secret')
    from datetime import datetime
    date = datetime(2014, 5, 5)
    d = ua.reports.DevicesReport(airship)
    devices = d.get(date)


Push Report
===========

Get the number of pushes you have sent within a specified time period.
For more information, see `the API documentation on Push Reports
<http://docs.urbanairship.com/api/ua.html#push-report>`_.

.. code-block:: python

    import urbanairship as ua
    from datetime import datetime

    airship = ua.Airship('appkey', 'master_secret')
    start_date = datetime(2015, 6, 1)
    end_date = datetime(2015, 7, 1)
    precision = 'HOURLY'
    listing = ua.reports.PushList(airship, start_date, end_date, precision)
    for resp in listing:
        print(resp.date, resp.android, resp.ios)

.. note::
    precision needs to be a member of ['HOURLY', 'DAILY', 'MONTHLY']


Response Report
===============

Get the number of direct and influenced opens of your app. For more 
information, see `the documentation on Response Report
<http://docs.urbanairship.com/api/ua.html#response-report>`__

.. code-block:: python

    import urbanairship as ua
    from datetime import datetime

    airship = ua.Airship('appkey', 'master_secret')
    start_date = datetime(2015, 6, 1)
    end_date = datetime(2015, 7, 1)
    precision = 'HOURLY'
    listing = ua.reports.ResponseReportList(
        airship,
        start_date,
        end_date,
        precision
    )
    for resp in listing:
        print(resp.date, resp.android['influenced'], resp.android['direct'],
            resp.ios['influenced'], resp.ios['direct'])

.. note::
    precision needs to be a member of ['HOURLY', 'DAILY', 'MONTHLY']


Response Listing
==================

Get a listing of all pushes and basic response information in a given
timeframe by instantiating an iterator object using ResponseList.
Start and end date times are required parameters.
For more information, see `the documentation on Response Listing
<http://docs.urbanairship.com/api/ua.html#response-listing>`__

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

.. note::
    limit (optional) is the number of results desired per page.
    push_id_start (optional) specifies the id of the first response to return.


App Opens Report
================

Get the number of users who have opened your app within the specified time 
period. For more information, see `the documentation on App Opens
<http://docs.urbanairship.com/api/ua.html#app-opens-report>`__

.. code-block:: python

    import urbanairship as ua
    from datetime import datetime

    airship = ua.Airship('appkey', 'master_secret')
    start_date = datetime(2015, 6, 1)
    end_date = datetime(2015, 7, 1)
    precision = 'HOURLY'
    listing = ua.reports.AppOpensList(airship, start_date, end_date, precision)
    for resp in listing:
        print(resp.date, resp.android, resp.ios)

.. note::
    precision needs to be a member of ['HOURLY', 'DAILY', 'MONTHLY']


Time In App Report
==================

Get the average amount of time users have spent in your app within the 
specified time period. For more information, see `the documentation on
Time In App Report
<http://docs.urbanairship.com/api/ua.html#time-in-app-report>`__

.. code-block:: python

    import urbanairship as ua
    from datetime import datetime

    airship = ua.Airship('appkey', 'master_secret')
    start_date = datetime(2015, 6, 1)
    end_date = datetime(2015, 7, 1)
    precision = 'HOURLY'
    listing = ua.reports.TimeInAppList(airship, start_date, end_date, precision)
    for resp in listing:
        print(resp.date, resp.android, resp.ios)

.. note::
    precision needs to be a member of ['HOURLY', 'DAILY', 'MONTHLY']


Opt-In Report
=============

Get the number of opted-in push users who access the app within the specified 
time period.
For more information, see `the documentation on Opt In Report
<http://docs.urbanairship.com/api/ua.html#opt-in-report>`__

.. code-block:: python

    import urbanairship as ua
    from datetime import datetime

    airship = ua.Airship('appkey', 'master_secret')
    start_date = datetime(2015, 6, 1)
    end_date = datetime(2015, 7, 1)
    precision = 'HOURLY'
    listing = ua.reports.OptInList(airship, start_date, end_date, precision)
    for resp in listing:
        print(resp.date, resp.android, resp.ios)

.. note::
    precision needs to be a member of ['HOURLY', 'DAILY', 'MONTHLY']


Opt-Out Report
==============
Get the number of opted-out push users who access the app within the specified 
time period.
For more information, see `the documentation on Opt Out Report
<http://docs.urbanairship.com/api/ua.html#opt-out-report>`__

.. code-block:: python

    import urbanairship as ua
    from datetime import datetime

    airship = ua.Airship('appkey', 'master_secret')
    start_date = datetime(2015, 6, 1)
    end_date = datetime(2015, 7, 1)
    precision = 'HOURLY'
    listing = ua.reports.OptOutList(airship, start_date, end_date, precision)
    for resp in listing:
        print(resp.date, resp.android, resp.ios)

.. note::
    precision needs to be a member of ['HOURLY', 'DAILY', 'MONTHLY']
