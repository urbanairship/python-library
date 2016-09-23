######
Passes
######


***********
Create Pass
***********

To `create a pass`_, use the ``Pass`` class' ``create`` method:

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')

   my_pass = ua.ApplePass()
   member_name = ua.Field(
       name='Member Name',
       value='First Last'
   )

   my_pass.add_fields(member_name)
   my_pass.set_expiration(datetime.datetime(2016, 12, 12))
   my_pass.set_public_url('multiple')
   response = my_pass.create(client, template_id=12345)


***********
Update Pass
***********

To `update a pass`_, use the ``Pass`` class' ``update`` method:

.. note::

   Unlike the template update endpoint, the pass update endpoint accepts partial
   updates. Consequently, you do not have to execute a get on the pass before
   update.

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')

   my_pass = ua.ApplePass()
   member_name = ua.Field(
       name='Member Name',
       value='First Last'
   )

   my_pass.add_fields(member_name)
   response = my_pass.update(client, template_id=12345)


********
Get Pass
********

To `get a pass`_, use the ``get_pass`` method:

.. code-block:: python

   import uareach as ua

   client = ua.Reach('email', 'api_key')

   my_pass = ua.get_pass(client, pass_id=12345)


***********
List Passes
***********

To get `a list of passes`_, use the ``PassList`` class:

.. code-block:: python

   import uareach as ua

   client = ua.Reach('email', 'api_key')

   pass_list = ua.TemplateList(client)

   for pass_ in pass_list:
      print pass_



***********
Delete Pass
***********

To `delete a pass`_, use the ``delete_pass`` method:

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')

   response = ua.delete_pass(client, pass_id=12345)


*********************
Add Locations to Pass
*********************

To `add locations to a pass`, use the ``add_pass_locations`` function:

.. code-block:: python

   import uareach as ua

   client = ua.Reach('email', 'api_key')

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

   ua.add_pass_locations(client, location_1, location_2, pass_id=12345)


*************************
Remove Location from Pass
*************************

To `delete a location from a pass`, use the ``delete_pass_location`` method:

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')


   ua.delete_pass_location(client, 1234567, pass_id=52431)


.. _create a pass: http://docs.urbanairship.com/api/wallet.html#create-pass
.. _update a pass: http://docs.urbanairship.com/api/wallet.html#update-pass
.. _get a pass: http://docs.urbanairship.com/api/wallet.html#get-pass
.. _a list of passes: http://docs.urbanairship.com/api/wallet.html#list-passes
.. _delete a pass: http://docs.urbanairship.com/api/wallet.html#delete-pass
.. _add locations to a pass: http://docs.urbanairship.com/api/wallet.html#add-locations-to-pass
.. _delete a location from a pass: http://docs.urbanairship.com/api/wallet.html#delete-location-from-pass
