import reach as ua
import os


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])


response = ua.duplicate_template(ua_reach, template_id=12345)
print response
