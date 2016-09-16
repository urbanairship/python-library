import wallet as ua
import os


ua_wallet = ua.Wallet("maxdelgiudice@gmail.com", os.environ['WALLET_KEY_RAW'])
pass_obj = ua.PassList(ua_wallet)


if __name__ == '__main__':
    for item in pass_obj:
        print item['serialNumber']
