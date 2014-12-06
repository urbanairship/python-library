import datetime
import unittest

import urbanairship as ua


class TestSchedule(unittest.TestCase):

    def test_scheduled_time(self):
        d = datetime.datetime(2013, 1, 1, 12, 56)
        self.assertEqual(ua.scheduled_time(d),
            {'scheduled_time': '2013-01-01T12:56:00'})

