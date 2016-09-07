import wallet as ua
import os
import json


ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])


# 1. Get the template
google_loyalty_template = ua.get_template(ua_wallet, template_id=53153)
print(json.dumps(google_loyalty_template._create_payload(), indent=4, sort_keys=True))
