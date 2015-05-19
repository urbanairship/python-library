import mock
import requests
import unittest

import urbanairship as ua


class TestSeries(unittest.TestCase):
    def test_invalid_precision(self):
        airship = ua.Airship('key', 'secret')
        s = ua.reports.PerPushSeries(airship)
        self.assertRaises(
            ValueError,
            callableObj=s.get_with_precision,
            push_id='push_id',
            precision='1'
        )

    def test_invalid_range(self):
        airship = ua.Airship('key', 'secret')
        s = ua.reports.PerPushSeries(airship)
        self.assertRaises(
            ValueError,
            callableObj=s.get_with_precision_and_range,
            push_id='push_id',
            precision='HOURLY',
            start='3/2/2015',
            end='3/5/2015'
        )


class TestDetail(unittest.TestCase):
    def test_get_single_with_empty_id(self):
        airship = ua.Airship('key', 'secret')
        d = ua.reports.PerPushDetail(airship)
        self.assertRaises(
            ValueError,
            callableObj=d.get_single,
            push_id=None
        )

    def test_get_batch_empty_list(self):
        airship = ua.Airship('key', 'secret')
        d = ua.reports.PerPushDetail(airship)
        self.assertRaises(
            ValueError,
            callableObj=d.get_batch,
            push_ids=[]
        )
