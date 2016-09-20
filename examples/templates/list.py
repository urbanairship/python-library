import reach as ua
import os


ua_reach = ua.Reach("me@example.com", os.environ['REACH_KEY_RAW'])
list_obj = ua.TemplateList(ua_reach)

for item in list_obj:
    print item
