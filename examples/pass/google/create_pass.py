import os
import json
import wallet as ua
import datetime


ua_wallet = ua.Wallet("maxdelgiudice@gmail.com", os.environ['WALLET_KEY_RAW'])


my_pass = ua.GooglePass()

gift_card_deetz = ua.Field(
    name='Gift Card Details',
    value='Will this work at least?',
    fieldType=ua.GoogleFieldType.TEXT_MODULE
)

my_pass.set_expiration(datetime.datetime(2016, 12, 12))
my_pass.set_public_url('multiple')
my_pass.add_fields(gift_card_deetz)
print json.dumps(my_pass._create_payload(), indent=4)

# Apple: 53438, Google: 53464
response = my_pass.create(ua_wallet, template_id=53438)
print response
