import wallet as ua
import os


ua_wallet = ua.Wallet("you@example.com", os.environ['WALLET_KEY_RAW'])

location = {
    "longitude": -80.1918,
    "latitude": 25.7617
}

response = ua.add_template_locations(ua_wallet, [location_2], template_id=52587)
print response
