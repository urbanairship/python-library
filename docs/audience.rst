Audience and Segmentation
**************************

Segments
========
Examples can be found in `the segments documentation here. <https://docs.airship.com/api/ua/?python#tag-segments>`_

.. autoclass:: urbanairship.devices.segment.Segment
    :members:
    :exclude-members: from_payload
    :noindex:

Segment Listing
---------------
Segment lists are fetched by instantiating an iterator object
using :py:class:`SegmentList`.

.. autoclass:: urbanairship.devices.segment.SegmentList
    :members:


Tags
=====
Examples can be found in `the tags documentation here. <https://docs.airship.com/api/ua/?python#tag-tags>`_

Channel Tags
------------

.. automodule:: urbanairship.devices.tag
    :members: ChannelTags

Open Channel Tags
------------------
.. autoclass:: urbanairship.devices.tag.OpenChannelTags
    :members:

Email Channel Tags
-------------------

.. autoclass:: urbanairship.devices.email.EmailTags
    :members:
    :noindex:

Named User Tags
----------------

.. autoclass:: urbanairship.devices.named_users.NamedUserTags
    :members:
    :inherited-members:
    :noindex:

Named User
===========
A Named User is a proprietary identifier that maps customer-chosen IDs, e.g., CRM data, to Channels. It is useful to think of a Named User as an individual consumer who might have more than one mobile device registered with your app.

Examples can be found in `the named users documentation here. <https://docs.airship.com/api/ua/?python#tag-named-users>`_

.. autoclass:: urbanairship.devices.named_users.NamedUser
    :members:

Named User List
---------------

.. autoclass:: urbanairship.devices.named_users.NamedUserList
    :members:
    :inherited-members:
    :noindex:

Attributes
===========
Define and manage attributes.

Examples can be found in `the attributes documentation here. <https://docs.airship.com/api/ua/?python#tag-attribute-lists>`_

.. autoclass:: urbanairship.devices.attributes.Attribute
    :members:

.. autoclass:: urbanairship.devices.attributes.ModifyAttributes
    :members:


Lists
======
Create and manage audience lists.

Attribute Lists
---------------
Examples can be found in `the attributes documentation here. <https://docs.airship.com/api/ua/?python#tag-attribute-lists>`_

.. autoclass:: urbanairship.devices.attributes.AttributeList
    :members:

Subscription Lists
-------------------
Examples can be found in `the subscription lists documentation here. <https://docs.airship.com/api/ua/?python#operation-api-channels-subscription_lists-post>`_

.. autoclass:: urbanairship.devices.subscription_lists.SubscriptionList
    :members:

Static Lists
------------
Examples can be found in `the static lists documentation here. <https://docs.airship.com/api/ua/?python#tag-static-lists>`_

.. autoclass:: urbanairship.devices.static_lists.StaticList
    :members:

.. autoclass:: urbanairship.devices.static_lists.StaticLists
    :members:
