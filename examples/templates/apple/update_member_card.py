import wallet as ua
import os

ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])

# 1. Get the template
apple_member_card_template = ua.get_template(ua_wallet, template_id=52344)

# 2. Update whatever
apple_member_card_template.remove_field('Merchant ID')

# 3. Update the template
response = apple_member_card_template.update(ua_wallet)
print response
