#########
Templates
#########


.. TODO: Get template will change -- update this when it does

************
Get Template
************

To `get a template`, use the ``get_template`` function.

.. code-block:: python

   import wallet as ua

   ua_wallet = ua.Wallet('email', 'api_key')
   myTemplate = ua.AppleTemplate.get_from_id(ua_wallet, template_id=12345)
   template_for_upload = existing_template.create_payload()


**************
List Templates
**************

To get `a list of templates`, use the ``TemplateList`` class:

.. code-block:: python

   import wallet as ua

   ua_wallet = ua.Wallet('email', 'api_key')
   template_list = ua.TemplateList(ua_wallet)

   for template_header in template_list:
      print template_header


*****************
Delete a Template
*****************

To `delete a template`,  use the ``delete_template`` function:

.. code-block:: python

   import wallet as ua


   ua_wallet = ua.Wallet('email', 'api_key')
   response = ua.delete_template(ua_wallet, template_id=12345)



********************
Duplicate a Template
********************

To `duplicate a template`, use the ``duplicate_template`` function.  This will
put the newly created template in the same project as the original:

.. code-block:: python

   import wallet as ua


   ua_wallet = ua.Wallet('email', 'api_key')
   response = ua.duplicate_template(ua_wallet, template_id=12345)


*************************
Add Locations to Template
*************************

To `add locations to a template`, use the ``add_template_locations`` function:

.. code-block:: python

   import wallet as ua


   ua_wallet = ua.Wallet('email', 'api_key')


   # Minimal location object
   location_1 = {
       "longitude": "-122.374",
       "latitude": "37.618"
   }

   # Full location object
   location_2 = {
       "longitude": "-80.1918",
       "latitude": "25.7617",
       "relevantText": "Hello loc 2",
       "streetAddress1": "address line #1",
       "streetAddress2": "address line #2",
       "city": "Miami",
       "region": "FL",
       "regionCode": "33101",
       "country": "US"
   }

   response = ua.add_template_locations(
       ua_wallet,
       [location_1, location_2]
       template_id=12345
   )


*****************************
Remove Location from Template
*****************************

To `remove a location from a template`, use the ``remove_template_location`` function:

.. code-block:: python

   import wallet as ua


   ua_wallet = ua.Wallet('email', 'api_key')
   response = ua.remove_template_location(
      ua_wallet,
      12345678,
      template_id=12345
   )


.. _get a template: http://docs.urbanairship.com/api/wallet.html#get-template
.. _a list of templates: http://docs.urbanairship.com/api/wallet.html#list-passes
.. _delete a template: http://docs.urbanairship.com/api/wallet.html#delete-template
.. _duplicate a template: http://docs.urbanairship.com/api/wallet.html#duplicate-template
.. _add locations to a template: http://docs.urbanairship.com/api/wallet.html#add-locations-to-template
.. _remove a location from a template: http://docs.urbanairship.com/api/wallet.html#delete-location-from-template
