import reach as ua
import os
import json


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])


# 1. Get the template
google_loyalty_template = ua.get_template(ua_reach, template_id=53153)
print(json.dumps(google_loyalty_template._create_payload(), indent=4, sort_keys=True))
