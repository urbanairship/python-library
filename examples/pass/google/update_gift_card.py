import os
import json
import reach as ua


ua_reach = ua.Reach("maxdelgiudice@gmail.com", os.environ['REACH_KEY_RAW'])

pass_ = ua.ApplePass()

balance = ua.Field(
    name='Balance',
    label=32.0,
    value='Bleep',
    currencyCode='USD',
    fieldType=ua.GoogleFieldType.TITLE_MODULE
)
pass_.add_fields(balance)

print(json.dumps(pass_._create_payload(), indent=4, sort_keys=True))
response = pass_.update(ua_reach, pass_id=20714020)
print response
