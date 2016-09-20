import reach as ua
import os
import json


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])

# 1. Get the template
google_coupon_template = ua.get_template(ua_reach, template_id=53151)
print(json.dumps(google_coupon_template._create_payload(), indent=4))

# 2. Update whatever field, headers, etc (look through source code to see available
# functions & examples)
member_name = google_coupon_template.fields['Member Name']
member_name['value'] = 'Firsty McLasterson'
member_name['changeMessage'] = 'Edited'

# 3. Update the template
response = google_coupon_template.create(ua_reach)
print response
