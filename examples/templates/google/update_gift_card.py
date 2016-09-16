import wallet as ua
import os
import json


ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])

# 1. Get the template
google_loyalty_template = ua.get_template(ua_wallet, template_id=53438)
print(json.dumps(google_loyalty_template.view(), indent=4))

del google_loyalty_template.top_level_fields['imageModulesData']

# 3. Update the template
response = google_loyalty_template.update(ua_wallet)
updated_template = ua.get_template(ua_wallet, template_id=53438)
print(json.dumps(updated_template.view(), indent=4))
