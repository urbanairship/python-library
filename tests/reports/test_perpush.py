import mock
import requests
import urbanairship as ua
import unittest


class TestSeries(unittest.TestCase):
    def test_invalid_precision(self):
        s = ua.Series()
        self.assertRaises(ValueError, s.get_with_precision,
                          None, 'push_id', '1')

    def test_invalid_range(self):
        s = ua.Series()
        self.assertRaises(ValueError,
                          s.get_with_precision_and_range,
                          None,
                          'push_id',
                          'HOURLY', '3/2/2015', '3/5/2015')
