import os
import json
import reach as ua


ua_reach = ua.Reach("maxdelgiudice@gmail.com", os.environ['REACH_KEY_RAW'])


pass_ = ua.get_pass(ua_reach, pass_id=18968249)
tier_field = pass_.fields['Tier']
tier_field['value'] = '3.0'


print(json.dumps(pass_.create_payload(), indent=4))
#response = pass_.update(ua_reach)
#print response
