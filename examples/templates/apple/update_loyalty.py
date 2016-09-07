import wallet as ua
import os


ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])

# 1. Get the template
apple_loyalty_template = ua.get_template(ua_wallet, template_id=52385)

# 2. Update whatever
points = apple_loyalty_template.fields['Points']
points['value'] = '123e2'
points['changeMessage'] = 'Edited'

# 3. Update the template
response = apple_loyalty_template.update(ua_wallet)
print response
