import wallet as ua
import os


ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])

location = {
    "longitude": -80.1918,
    "latitude": 25.7617
}

response = ua.add_template_locations(
    ua_wallet,
    [location],
    template_id=52587
)

print response
