import wallet as ua
import os


ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])


response = ua.delete_template(ua_wallet, template_id=12345)
print response
