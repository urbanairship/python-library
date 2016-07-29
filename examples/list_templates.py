import wallet as ua
import os


ua_wallet = ua.Wallet("maxdelgiudice@gmail.com", os.environ['WALLET_KEY_RAW'])


list_obj = ua.TemplateList(ua_wallet)

for item in list_obj:
    print item
