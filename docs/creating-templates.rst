###################
Template Operations
###################

The process for creating or updating a template via the python library consists
of 3 steps:

* Add/remove/set template headers
* Add/remove/set template metadata
* Add/remove/set template fields

This tutorial explains the relevant classes, methods, and enums for accomplishing
the above tasks. In the code samples throughout the tutorial, we assume that the
following imports/constants are defined:

.. sourcecode:: python

   import reach as ua

   client = ua.Reach('you@example.com', 'reach-key')

   # Initialize the template -- in this example, we create an apple template.
   my_template = ua.AppleTemplate()


********
Metadata
********

When manipulating a template, you'll use the one of the following methods to
update the template metadata:

.. sourcecode:: python

   # Add metadata to the template
   my_template.add_metadata(name='A template')

   # Remove metadata from the template
   my_template.remove_metadata('name')

   # Set the template metadata (remove all currently existing metadata, and
   # add the specified key/values)
   my_template.set_metadata(name='A template', description='Template description')

The table below contains a full listing of available keys for the ``metadata`` methods:

================= ======================================================================================================= =====================================
Key               Description                                                                                             Required
================= ======================================================================================================= =====================================
``name``          The name of the template.                                                                               Yes
``vendor``        One of ``'apple'`` or ``'google'``. Set automatically by the library.                                   Yes (set automatically)
``vendorId``      One of ``1`` or ``2``. Set automatically by the library.                                                Yes (set automatically)
``project_type``  The type of the project. See `template_type`_ for options.                                              Yes (alternatively can use ``type_``)
``template_type`` The type of the template. See `project_type`_ for options.                                              Yes (alternatively can use ``type_``)
``type_``         Helper key -- allows you to set project_type and template_type simultaneously. See `type`_ for details. No
``deleted``       A boolean representing whether the template is deleted.                                                 No
``description``   A description for the template.                                                                         No
``disabled``      A boolean representing whether the template is disabled.                                                No
``template_id``   The template ID.                                                                                        No
``project_id``    The ID of the project associated with the template.                                                     No
================= ======================================================================================================= =====================================

.. note::

   You will either specify both ``project_type`` and ``template_type``, or you can
   use the streamlined ``type_`` key which takes care of setting the two former keys
   for you.

.. note::

   When using the ``remove_metadata`` method, you must pass in the Key values as strings
   (e.g., ``'name'``, ``'description'``, etc).


template_type
=============

The table below lists possible values for the ``template_type`` key. You can use either
the provided constant or the associated string:

============================== ===================
Constant                       Associated String
============================== ===================
``TemplateType.BOARDING_PASS`` ``'Boarding Pass'``
``TemplateType.COUPON``        ``'Coupon'``
``TemplateType.EVENT_TICKET``  ``'Event Ticket'``
``TemplateType.GENERIC``       ``'Generic'``
``TemplateType.STORE_CARD``    ``'Store Card'``
``TemplateType.LOYALTY``       ``'Loyalty'``
``TemplateType.OFFER``         ``'Offer'``
``TemplateType.GIFT_CARD``     ``'Gift Card'``
============================== ===================


project_type
============

The table below lists possible values for the ``project_type`` key. You can use either
the provided constant or the associated string:

============================= ===================
Constant                      Associated String
============================= ===================
``ProjectType.BOARDING_PASS`` ``'boardingPass'``
``ProjectType.COUPON``        ``'coupon'``
``ProjectType.EVENT_TICKET``  ``'eventTicket'``
``ProjectType.GENERIC``       ``'generic'``
``ProjectType.LOYALTY``       ``'loyalty'``
``ProjectType.GIFT_CARD``     ``'giftCard'``
``ProjectType.MEMBER_CARD``   ``'MemberCard'``
============================= ===================


type
====

The ``type_`` key provides an alternative to setting both ``project_type`` and
``template_type``. You can choose from one of the options listed below:

+------------------------+
| Type Constant          |
+========================+
| ``Type.LOYALTY``       |
+------------------------+
| ``Type.COUPON``        |
+------------------------+
| ``Type.GIFT_CARD``     |
+------------------------+
| ``Type.MEMBER_CARD``   |
+------------------------+
| ``Type.EVENT_TICKET``  |
+------------------------+
| ``Type.BOARDING_PASS`` |
+------------------------+
| ``Type.GENERIC``       |
+------------------------+


*******
Headers
*******

Template headers specify high-level template options -- associated images, template
colors, and barcode options are all specified via headers. Available operations
on template headers mirror those available for metadata:

.. sourcecode:: python

   # Add headers to the template
   apple_coupon.add_headers(
       barcode_type='BarcodeFormatPDF417',
       logo_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-logo.png',
       background_color=ua.rgb(0, 147, 201),
       logo_color=ua.rgb(24, 86, 148),
       foreground_color=ua.rgb(255, 255, 255),
   )

   # Remove headers from the template
   my_template.remove_headers('logo_image')

   # Set the template headers (remove all currently existing metadata, and
   # add the specified key/values)
   my_template.set_headers(
       background_color=ua.rgb(0, 147, 201),
       logo_color=ua.rgb(24, 86, 148),
       foreground_color=ua.rgb(255, 255, 255)
   )

See below for a complete listing of available headers:

======================== ====================================================================================
Key                      Description
======================== ====================================================================================
``background_color``     The background color of the template.
``background_image``     The background image of the template.
``barcodeAltText``       The text that displays below the barcode.
``barcode_encoding``     The barcode encoding type. Use ``'iso-8859-1'``
``barcode_type``         The barcode type. See `barcode_type`_ for available options.
``barcode_value``        The actual value represented by the barcode.
``footer_image``         Link to image to display in the template footer.
``foreground_color``     Specify the template foreground color.
``icon_image``           Specify the template icon image.
``logo_color``           Specify the template logo color (Apple only).
``logo_image``           Specify the template logo image.
``logo_text``            Specify the text under the template logo.
``strip_image``          Specify the barcode strip image.
``suppress_strip_shine`` A boolean -- Suppress the strip shine effect on barcodes.
``thumbnail_image``      A URL specifying the thumbnail image.
``transitType``          Only used with boarding pass. See `transitType (Apple Only)`_ for available options.
======================== ====================================================================================


barcode_type
============

See below for a full listing of ``barcode_type`` values. Note that some
barcode types are only available for Google templates.

======================== ================= ===== ======
Constant                 Associated String Apple Google
======================== ================= ===== ======
``BarcodeType.PDF_417``  ``'PDF_417'``     Yes   Yes
``BarcodeType.AZTEC``    ``'AZTEC'``       Yes   Yes
``BarcodeType.QR_CODE``  ``'QR_CODE'``     Yes   Yes
``BarcodeType.CODE_128`` ``'CODE_128'``    Yes   Yes
``BarcodeType.UPC_A``    ``'UPC_A'``       No    Yes
``BarcodeType.EAN_13``   ``'EAN_13'``      No    Yes
``BarcodeType.CODE_39``  ``'CODE_39'``     No    Yes
======================== ================= ===== ======


transitType (Apple Only)
========================

Transit type is used to specify the type of transportation on
an on Apple Boarding Pass. See below for a full listing of
``transitType`` values:

======================= ========================
Constant                Associated String
======================= ========================
``TransitType.GENERIC`` ``'transitTypeGeneric'``
``TransitType.BUS``     ``'transitTypeBus'``
``TransitType.AIR``     ``'transitTypeAir'``
``TransitType.BOAT``    ``'transitTypeBoat'``
``TransitType.TRAIN``   ``'transitTypeTrain'``
======================= ========================


******
Fields
******

The Python Library uses a single field class for both Apple and Google templates.

The ``Field`` class is used to build fields. Let's look at a simple example:

.. code-block:: python

   program_name = ua.Field(
       name='Program Name',
       label='Program Name',
       value='Loyalty Points',
       fieldType=ua.AppleFieldType.PRIMARY
   )

Note that the only thing that distinguishes this as a field for an Apple Template is
the ``fieldType`` value. Aside from a handful of Google and Apple-specific keys, Apple
and Google field definitions will usually look similar. Here is a roughly analagous field
definition for a Google field:

.. code-block:: python

   loyalty_program = ua.Field(
       name='Program Name',
       label='Program Name',
       value='Loyalty Points',
       fieldType=ua.GoogleFieldType.TITLE_MODULE
   )

Here is a complete listing of valid keys for ``Field``:

============================ ====================== ============ =================================================================================================== =====================================================================================================
Key                          Value Type             Apple/Google Description                                                                                         Additional Notes
============================ ====================== ============ =================================================================================================== =====================================================================================================
``name``                     String                 Both         The name used to refer to the field.
``label``                    String                 Both         The label of the field -- generally describes the field value.
``value``                    String, Int, or Float  Both         The value of the field.
``fieldType``                String                 Both         The location of the field on the template. See `fieldTypes`_ for options.
``changeMessage``            String                 Both         The message to display if the field is updated.
``formatType``               String                 Both         The type of value. See `formatType`_ for options.                                                   The python library will attempt to determine this automatically
``hideEmpty``                Boolean                Both         Hide the field if no value is specified.
``order``                    Int                    Both         Specify location within the ``fieldType``.
``required``                 Boolean                Both         Whether the field must be defined when creating passes from the template.
``currencyCode``             String                 Both         If making a field with a currency value, specify the denomination. See `currencyCode`_ for options. If you set ``currencyCode``, ``formatType`` will be set to ``"Currency`` unless you manually override
``textAlignment``            String                 Both         Specify how text is aligned within the field. See `textAlignment` for options.
``numberStyle``              String                 Apple        If ``value`` is a number, specify the number type. See `numberStyle`_ for options.                  The python library will attempt to determine this automatically
``row``                      Int                    Google       Specify vertical location within the ``fieldType``.                                                 Deprecated, please use ``order`` if possible
``col``                      Int                    Google       Specify horizontal location within the ``fieldType``.                                               Deprecated, please use ``order`` if possible
============================ ====================== ============ =================================================================================================== =====================================================================================================

.. note::

   While the ``formatType`` and ``numberStyle`` keys will be set automatically, you can always
   override them. The python library will do its best to guess and should be correct in most
   situations, but there may be edge cases where you have to override set these values
   explicitly.


formatType
==========

The ``formatType`` key specifies the type of argument passed to ``value``. Generally, the
library can deduce the ``formatType`` without user intervention. However, ``'Phone'`` and
``'Email'`` will always have to be specified by the user.

======================= =================
Constant                Associated String
======================= =================
``FormatType.NUMBER``   ``'Number'``
``FormatType.STRING``   ``'String'``
``FormatType.URL``      ``'URL'``
``FormatType.DATE``     ``'Date'``
``FormatType.CURRENCY`` ``'Currency'``
``FormatType.PHONE``    ``'Phone'``
``FormatType.EMAIL``    ``'Email'``
======================= =================


fieldTypes
==========

The ``fieldType`` key specifies the location of a field on an Apple or Google
template. The available fieldTypes are listed below:

**Google fieldTypes:**

================================== =====================
Constant                           Associated String
================================== =====================
``GoogleFieldType.INFO_MODULE``    ``'infoModuleData'``
``GoogleFieldType.TEXT_MODULE``    ``'textModulesData'``
``GoogleFieldType.LINKS_MODULE``   ``'linksModuleData'``
``GoogleFieldType.POINTS_MODULE``  ``'pointsModule'``
``GoogleFieldType.NOT_ASSIGNED``   ``'notAssigned'``
``GoogleFieldType.TITLE_MODULE``   ``'titleModule'``
``GoogleFieldType.ACCOUNT_MODULE`` ``'acctModule'``
``GoogleFieldType.LOYALTY_POINTS`` ``'loyaltyPoints'``
================================== =====================

**Apple fieldTypes:**

=============================== =================
Constant                        Associated String
=============================== =================
``AppleFieldType.PRIMARY``      ``'primary'``
``AppleFieldType.SECONDARY``    ``'secondary'``
``AppleFieldType.TERTIARY``     ``'tertiary'``
``AppleFieldType.AUXILIARY``    ``'auxiliary'``
``AppleFieldType.BACK``         ``'back'``
``AppleFieldType.HEADER``       ``'header'``
``AppleFieldType.NOT_ASSIGNED`` ``'notAssigned'``
=============================== =================


numberStyle (Apple Only)
========================

The ``numberStyle`` key must be specified for Apple fields with a
``formatType`` of ``'Number'``. Usually, the library can deduce
the appropriate ``numberStyle`` based on the ``value`` argument, but
there still may be situations where it is useful to manually
override the ``numberStyle`` key.

========================== ===========================
Constant                   Assocaited String
========================== ===========================
``NumberStyle.DECIMAL``    ``'numberStyleDecimal'``
``NumberStyle.TEXT``       ``'numberStyleSpellOut'``
``NumberStyle.SCIENTIFIC`` ``'numberStyleScientific'``
``NumberStyle.PERCENT``    ``'numberStylePercent'``
========================== ===========================


textAlignment
=============

Specify the alignment of the field text:

========================== ==========================
Constant                   Associated String
========================== ==========================
``TextAlignment.LEFT``     ``'textAlignmentLeft'``
``TextAlignment.CENTER``   ``'textAlignmentCenter'``
``TextAlignment.RIGHT``    ``'textAlignmentRight'``
``TextAlignment.NATURAL``  ``'textAlignmentNatural'``
========================== ==========================


currencyCode
============

Specify the type of currency for ``Currency`` fields:

==================== =================
Constant             Associated String
==================== =================
``CurrencyCode.USD`` ``'USD'``
``CurrencyCode.EUR`` ``'EUR'``
``CurrencyCode.CNY`` ``'CNY'``
``CurrencyCode.JPY`` ``'JPY'``
``CurrencyCode.GBP`` ``'GBP'``
``CurrencyCode.RUB`` ``'RUB'``
``CurrencyCode.AUD`` ``'AUD'``
``CurrencyCode.CHF`` ``'CHF'``
``CurrencyCode.CAD`` ``'CAD'``
``CurrencyCode.HKD`` ``'HKD'``
``CurrencyCode.SEK`` ``'SEK'``
``CurrencyCode.NZD`` ``'NZD'``
``CurrencyCode.KRW`` ``'KRW'``
``CurrencyCode.SGD`` ``'SGD'``
``CurrencyCode.NOK`` ``'NOK'``
``CurrencyCode.MXN`` ``'MXN'``
``CurrencyCode.INR`` ``'INR'``
==================== =================


*******************
Apple Only Features
*******************

These methods are specific to the AppleTemplate class.

Beacons
=======

To manipulate beacons on a template, use one of the following AppleTemplate methods:

.. sourcecode:: python

   # Add a beacon
   my_template.add_beacon(
      '55502220-A123-A88A-F321-555A444B333C',      # UUID
      relevantText="Hey you're in a cool place",   # Text displayed on lock screen
      major=1,                                     # Major beacon identifier
      minor=34                                     # Minor beacon identifier
   )

   # Remove a beacon (takes a UUID as argument)
   my_template.remove_beacon('55502220-A123-A88A-F321-555A444B333C')


********************
Google Only Features
********************

These methods are specific to the GoogleTemplate class.


Offer Module
============

When creating a Google coupon, you can specify an ``offerModule``. To do so,
use the ``set_offer`` method:

.. sourcecode:: python

   my_template.set_offer(
      multiUserOffer=False,
      redemptionChannel='both',
      provider='The provider',
      endTime='2017-01-30T00:00:00.000Z'
   )

Valid arguments are listed below:

===================== ======================================================================================================================================
Key                   Description
===================== ======================================================================================================================================
``multiUserOffer``    If true, this offer can be saved by multiple users. Otherwise, the offer is only available for a single user.
``redemptionChannel`` Redemption channels applicable to this offer. Can be one of ``'online'``, ``'instore'``, ``'both'``, or ``'temporaryPriceReduction'``.
``provider``          The provider name.
``endTime``           The offer expiration date.
===================== ======================================================================================================================================


Message Module Field
====================

To add a message to your template, use the ``add_message`` method:

.. sourcecode:: python

   my_template.add_message(
       body='A new message!',
       imageUri='https://imgur.com/cool_image.png'
   )

Valid arguments are listed below:

======================== ======== ==============================================================
Key                      Required Description
======================== ======== ==============================================================
``body``                 Yes      The message body.
``header``               No       The message title.
``actionUri``            No       The URI to which users are directed upon clicking the message.
``actionUriDescription`` No       Description for the ``actionUri``.
``imageUri``             No       Specify an image to display with the message.
``imageDescription``     No       Description for the image.
``startTime``            No       Valid ISO8805 date for start time of a message.
``endTime``              No       Valid ISO8805 date for end time of a message.
======================== ======== ==============================================================
