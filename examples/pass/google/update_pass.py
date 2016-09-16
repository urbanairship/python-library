import os
import json
import wallet as ua


ua_wallet = ua.Wallet("maxdelgiudice@gmail.com", os.environ['WALLET_KEY_RAW'])


pass_ = ua.get_pass(ua_wallet, pass_id=18968249)
tier_field = pass_.fields['Tier']
tier_field['value'] = '3.0'


print(json.dumps(pass_.create_payload(), indent=4))
#response = pass_.update(ua_wallet)
#print response
