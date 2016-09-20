import os
import json
import sys
import reach as ua
import datetime


ua_reach = ua.Reach("maxdelgiudice@gmail.com", os.environ['REACH_KEY_RAW'])
pass_ = ua.get_pass(ua_reach, pass_id=sys.argv[1])
print json.dumps(pass_.view(), indent=4, sort_keys=True)
print json.dumps(pass_._create_payload(), indent=4)
