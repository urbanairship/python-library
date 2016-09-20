import reach as ua
import os


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])

location = {
    "longitude": -80.1918,
    "latitude": 25.7617
}

response = ua.add_template_locations(
    ua_reach,
    [location],
    template_id=52587
)

print response
