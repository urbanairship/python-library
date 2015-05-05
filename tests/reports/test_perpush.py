import mock
import requests
import urbanairship as ua
import unittest


class TestSeries(unittest.TestCase):
    def test_invalid_precision(self):
        s = ua.Series(None)
        self.assertRaises(ValueError,
                          callableObj=s.get_with_precision,
                          push_id='push_id',
                          precision='1')

    def test_invalid_range(self):
        s = ua.Series(None)
        self.assertRaises(ValueError,
                          callableObj=s.get_with_precision_and_range,
                          push_id='push_id',
                          precision='HOURLY',
                          start='3/2/2015',
                          end='3/5/2015')


class TestDetail(unittest.TestCase):
    def test_get_single_invalid_id_type(self):
        d = ua.Detail(None)
        self.assertRaises(TypeError,
                          callableObj=d.get_single,
                          push_id=12345)

    def test_get_single_with_empty_id(self):
        d = ua.Detail(None)
        self.assertRaises(ValueError,
                          callableObj=d.get_single,
                          push_id=None)

    def test_get_batch_empty_list(self):
        d = ua.Detail(None)
        self.assertRaises(ValueError,
                          callableObj=d.get_batch,
                          push_ids=[])
