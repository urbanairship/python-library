import os
import json
import wallet as ua
import datetime


ua_wallet = ua.Wallet("maxdelgiudice@gmail.com", os.environ['WALLET_KEY_RAW'])


my_pass = ua.Pass()


passenger = ua.Field(
    name='Passenger',
    value='Max Del Giudice'
)

my_pass.add_fields(passenger)
my_pass.set_expiration(datetime.datetime(2016, 12, 12))
my_pass.set_public_url('multiple')
print json.dumps(my_pass._create_payload(), indent=4, sort_keys=True)
response = my_pass.create(ua_wallet, template_id=53258)
print response
