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


.. _getting a pass: http://docs.urbanairship.com/api/wallet.html#get-pass
.. _delete a pass: http://docs.urbanairship.com/api/wallet.html#delete-pass
