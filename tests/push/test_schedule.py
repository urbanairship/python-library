import datetime
import unittest

import urbanairship as ua


class TestSchedule(unittest.TestCase):

    def test_scheduled_time(self):
        d = datetime.datetime(2013, 1, 1, 12, 56)
        self.assertEqual(
            ua.scheduled_time(d),
            {'scheduled_time': '2013-01-01T12:56:00'}
        )

    def test_local_scheduled_time(self):
        d = datetime.datetime(2015, 1, 1, 12, 56)
        self.assertEqual(
            ua.local_scheduled_time(d),
            {'local_scheduled_time': '2015-01-01T12:56:00'}
        )

