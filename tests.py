from ConfigParser import RawConfigParser
import unittest


class iOSTest(unittest.TestCase):
  def setUp(self):
    conf = RawConfigParser()
    conf.read('keys.ini')
    self.UA_MASTER_SECRET = conf.get('keys', 'UA_MASTER_SECRET')
    self.UA_APPLICATION_SECRET = conf.get('keys', 'UA_APPLICATION_SECRET')

  def testKeys(self):
    print self.UA_MASTER_SECRET
    print self.UA_APPLICATION_SECRET
  

if __name__ == '__main__':
  unittest.main()

