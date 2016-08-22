import wallet as ua
import os


ua_wallet = ua.Wallet("you@example.com", os.environ['WALLET_KEY_RAW'])


response = ua.duplicate_template(ua_wallet, template_id=52412)
print response
