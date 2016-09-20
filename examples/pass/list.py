import reach as ua
import os


ua_reach = ua.Reach("maxdelgiudice@gmail.com", os.environ['REACH_KEY_RAW'])
pass_obj = ua.PassList(ua_reach)


if __name__ == '__main__':
    for item in pass_obj:
        print item['serialNumber']
