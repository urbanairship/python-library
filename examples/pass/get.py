import os
import json
import sys
import wallet as ua
import datetime


ua_wallet = ua.Wallet("maxdelgiudice@gmail.com", os.environ['WALLET_KEY_RAW'])
pass_ = ua.get_pass(ua_wallet, pass_id=sys.argv[1])
print json.dumps(pass_.view(), indent=4, sort_keys=True)
print json.dumps(pass_._create_payload(), indent=4)
