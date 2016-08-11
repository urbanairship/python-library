######
Passes
######


********
Get Pass
********

To `get a pass`_, use the ``get_pass`` method:

.. code-block:: python

   import wallet as ua

   ua_wal = ua.Wallet('email', 'api_key')
   my_pass = ua.get_pass(ua_wal, pass_id='pass_id')


***********
Delete Pass
***********

To `delete a pass`_, use the ``delete_pass`` method:

.. code-block:: python

   import wallet as ua


   ua_wal = ua.Wallet('email', 'api_key')
   my_pass = ua.delete_pass(ua_wal, pass_id='pass_id')


*********************
Add Locations to Pass
*********************

To `add locations to a pass`, use the ``add_pass_locations`` function:

.. code-block:: python

   import wallet as ua

   ua_wal = ua.Wallet('email', 'api_key')

   location_1 = {
       "longitude":-122.374,
       "latitude":37.618,
       "relevantText":"Hello loc 1",
       "streetAddress1":"address line #1",
       "streetAddress2":"address line #2",
       "city":"Palo Alto",
       "region":"CA",
       "regionCode":"94404",
       "country":"US"
   }

   location_2 = {
       "longitude":134.25,
       "latitude":58.18,
       "relevantText":"Hello loc 2",
       "streetAddress1":"address line #1",
       "streetAddress2":"address line #2",
       "city":"Juneau",
       "region":"AK",
       "country":"US"
   }

   ua.add_pass_locations(ua_wal, location_1, location_2, pass_id=12345)


*************************
Remove Location from Pass
*************************

To `delete a location from a pass`, use the ``delete_pass_location`` method:

.. code-block:: python

   import wallet as ua


   ua_wal = ua.Wallet('email', 'api_key')


   ua.delete_pass_location(ua_wal, 1234567, pass_id=52431)


.. _getting a pass: http://docs.urbanairship.com/api/wallet.html#get-pass
.. _delete a pass: http://docs.urbanairship.com/api/wallet.html#delete-pass
.. _add locations to a pass: http://docs.urbanairship.com/api/wallet.html#add-locations-to-pass
.. _delete a location from a pass: http://docs.urbanairship.com/api/wallet.html#delete-location-from-pass
