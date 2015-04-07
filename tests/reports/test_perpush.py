import mock
import requests
import urbanairship as ua
import unittest


class TestSeries(unittest.TestCase):
    def test_invalid_precision(self):
        s = ua.Series()
        self.assertRaises(ValueError,
                          callableObj=s.get_with_precision,
                          airship=None,
                          push_id='push_id',
                          precision='1')

    def test_invalid_range(self):
        s = ua.Series()
        self.assertRaises(ValueError,
                          callableObj=s.get_with_precision_and_range,
                          airship=None,
                          push_id='push_id',
                          precision='HOURLY',
                          start='3/2/2015',
                          end='3/5/2015')


class TestDetail(unittest.TestCase):
    def test_get_single_invalid_id_type(self):
        d = ua.Detail()
        self.assertRaises(TypeError,
                          callableObj=d.get_single,
                          airship=None,
                          push_id=12345)

    def test_get_single_with_empty_id(self):
        d = ua.Detail()
        self.assertRaises(ValueError,
                          callableObj=d.get_single,
                          airship=None,
                          push_id=None)

    def test_get_batch_empty_list(self):
        d = ua.Detail()
        self.assertRaises(ValueError,
                          callableObj=d.get_batch,
                          airship=None,
                          push_ids=[])