#########
Templates
#########


.. TODO: Get template will change -- update this when it does

************
Get Template
************

Documentation on `getting a template`_.

.. code-block:: python

   import wallet as ua

   ua_wallet = ua.Wallet("email", "api_key")
   myTemplate = ua.AppleTemplate.get_from_id(ua_wallet, "template_id")
   template_for_upload = existing_template.create_payload())


**************
List Templates
**************

To get `a list of templates`, use the ``TemplateList`` class:

.. code-block:: python

   import wallet as ua

   ua_wallet = ua.Wallet("email", "api_key")
   template_list = ua.TemplateList(ua_wallet)

   for template_header in template_list:
      print template_header


.. _a list of templates: http://docs.urbanairship.com/api/wallet.html#list-passes
.. _getting a template: http://docs.urbanairship.com/api/wallet.html#get-template
