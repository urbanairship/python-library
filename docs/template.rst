Templates
=========

Get Template From Template ID
-----------------------------
Documentation on `getting a template`_.

.. code-block:: python

import wallet as ua

ua_wallet = ua.Wallet("email", "api_key")
myTemplate = ua.AppleTemplate.get_from_id(ua_wallet, "template_id")
template_for_upload = existing_template.create_payload())

.. _getting a template: http://docs.urbanairship.com/api/wallet.html#get-template