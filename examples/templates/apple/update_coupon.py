import wallet as ua
import os


ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])

# 1. Get the template
apple_coupon = ua.get_template(ua_wallet, template_id=52336)

# 2. Update/add/remove whatever
member = ua.Field(
    name='Member Name',
    label='Member Name',
    value='Firsty McLasterson',
    fieldType=ua.AppleFieldType.SECONDARY,
    order=3
)

apple_coupon.add_fields(member)

# 3. Update the template
response = apple_coupon.update(ua_wallet)
print response
