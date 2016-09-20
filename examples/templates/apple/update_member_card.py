import reach as ua
import os

ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])

# 1. Get the template
apple_member_card_template = ua.get_template(ua_reach, template_id=52344)

# 2. Update whatever
apple_member_card_template.remove_field('Merchant ID')

# 3. Update the template
response = apple_member_card_template.update(ua_reach)
print response
