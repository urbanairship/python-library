import reach as ua
import os
import json


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])

# 1. Get the template
google_loyalty_template = ua.get_template(ua_reach, template_id=53438)
print(json.dumps(google_loyalty_template.view(), indent=4))

del google_loyalty_template.top_level_fields['imageModulesData']

# 3. Update the template
response = google_loyalty_template.update(ua_reach)
updated_template = ua.get_template(ua_reach, template_id=53438)
print(json.dumps(updated_template.view(), indent=4))
