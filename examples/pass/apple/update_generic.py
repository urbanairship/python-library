import datetime
import json
import os
import sys

import reach as ua


ua_reach = ua.Reach("maxdelgiudice@gmail.com", os.environ['REACH_KEY_RAW'])

my_pass = ua.ApplePass()

balance = ua.Field(
    name='Balance', value='27.56'
)

my_pass.add_fields(balance)
my_pass.set_expiration(datetime.datetime(2016, 12, 12))
my_pass.set_public_url('multiple')
print json.dumps(my_pass._create_payload(), indent=4, sort_keys=True)
response = my_pass.update(ua_reach, pass_id=sys.argv[1])
print response
