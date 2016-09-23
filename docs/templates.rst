#########
Templates
#########


***************
Create Template
***************

.. note::

   The template creation process via the python library deviates from template
   creation through cURL requests. For details on constructing a template using
   the python library, please see :doc:`creating-templates`.

To `create a template`_, use the ``Template`` class' ``create`` method:

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')

   # 1. Initialize an Apple template; add metadata like name, description, etc
   apple_loyalty = ua.AppleTemplate()
   apple_loyalty.add_metadata(
       name='An Apple template',
       description='Rewards points',
       type_=ua.Type.LOYALTY
   )

   # 2. Add template headers
   apple_loyalty.add_headers(
       barcode_value='123456789',
       icon_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-icon.png',
       barcode_type=ua.BarcodeType.PDF_417,
       logo_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-logo.png',
       background_color=ua.rgb(49,159,196),
       barcode_encoding='iso-8859-1',
       logo_color=ua.rgb(24,86,148),
       barcodeAltText='123456789',
       foreground_color=ua.rgb(255,255,255),
       logo_text='Logo Text'
   )

   # 3. Create and add some fields
   program_name = ua.Field(
       name='Program Name',
       label='Bleep',
       value='Program Name',
       fieldType=ua.AppleFieldType.PRIMARY
   )

   points = ua.Field(
       name='Points',
       label='Points',
       value=1234.0,
       fieldType=ua.AppleFieldType.HEADER
   )

   apple_loyalty.add_fields(
      program_name,
      points
   )

   # 4. Call the create method
   response = my_template.create(client, project_id=12345)


***************
Update Template
***************

To `update a template`, use the ``Template`` class' ``update`` method:

.. code-block:: python

   import uareach as ua

   client = ua.Reach('email', 'api_key')

   # 1. Get a template to update
   my_template = ua.get_template(client, template_id=12345)

   # 2. Example: Update the template's 'Member Name' field
   member_name = my_template.fields['Member Name']
   member_name['value'] = 'The Biebz'

   # 3. Call the update method on the reach instance
   response = my_template.update(client)

.. note::

   As the example above shows, when updating a key-value pair within a
   field, you can just treat the field as a dictionary. To remove or create
   new fields/headers/metadata, you can use the methods described in the
   :doc:`creating-templates` doc.


************
Get Template
************

To `get a template`_, use the ``get_template`` function:

.. code-block:: python

   import uareach as ua

   client = ua.Reach('email', 'api_key')
   my_template = ua.get_template(client, template_id=12345)


**************
List Templates
**************

To get `a list of templates`_, use the ``TemplateList`` class:

.. code-block:: python

   import uareach as ua

   client = ua.Reach('email', 'api_key')

   template_list = ua.TemplateList(client)

   for template_header in template_list:
      print template_header


*****************
Delete a Template
*****************

To `delete a template`_,  use the ``delete_template`` function:

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')
   response = ua.delete_template(client, template_id=12345)



********************
Duplicate a Template
********************

.. note::

   Currently, this API call only works with Apple templates

To `duplicate a template`_, use the ``duplicate_template`` function.  This will
put the newly created template in the same project as the original:

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')
   response = ua.duplicate_template(client, template_id=12345)


*************************
Add Locations to Template
*************************

To `add locations to a template`_, use the ``add_template_locations`` function:

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')

   # Minimal location object
   location_1 = {
       "longitude": -122.374,
       "latitude": 37.618
   }

   # Full location object
   location_2 = {
       "longitude": -80.1918,
       "latitude": 25.7617,
       "relevantText": "Hello loc 2",
       "streetAddress1": "address line #1",
       "streetAddress2": "address line #2",
       "city": "Miami",
       "region": "FL",
       "regionCode": 33101,
       "country": "US"
   }

   response = ua.add_template_locations(
       client, [location_1, location_2], template_id=12345
   )


*****************************
Remove Location from Template
*****************************

To `remove a location from a template`_, use the ``remove_template_location`` function:

.. code-block:: python

   import uareach as ua


   client = ua.Reach('email', 'api_key')
   response = ua.remove_template_location(
      client, 12345678, template_id=12345
   )

.. _create a template: http://docs.urbanairship.com/api/wallet.html#create-template
.. _get a template: http://docs.urbanairship.com/api/wallet.html#get-template
.. _a list of templates: http://docs.urbanairship.com/api/wallet.html#list-passes
.. _delete a template: http://docs.urbanairship.com/api/wallet.html#delete-template
.. _duplicate a template: http://docs.urbanairship.com/api/wallet.html#duplicate-template
.. _add locations to a template: http://docs.urbanairship.com/api/wallet.html#add-locations-to-template
.. _remove a location from a template: http://docs.urbanairship.com/api/wallet.html#delete-location-from-template
