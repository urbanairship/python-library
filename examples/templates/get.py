import os
import sys
import json

import wallet as ua


ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])

# 1. Get the template
apple_gift_card = ua.get_template(ua_wallet, template_id=sys.argv[1])
response = apple_gift_card.create(ua_wallet)
print response

try:
    type_ = sys.argv[2]
except IndexError:
    type_ = 'view'

if type_ == 'view':
    print json.dumps(apple_gift_card.view(), indent=4, sort_keys=True)
elif type_ == 'create':
    print json.dumps(apple_gift_card._create_payload(), indent=4, sort_keys=True)
else:
    raise ValueError('Unrecognized method: {}'.format(type_))
