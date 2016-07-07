######
Passes
######

********
Get Pass
********

Documentation on `getting a pass`_.

.. code-block:: python

from wallet import Pass, Wallet

ua_wal = Wallet('email', 'api_key')
my_pass = Pass.get_pass(ua_wal, pass_id='pass_id')

.. _getting a pass: http://docs.urbanairship.com/api/wallet.html#get-pass