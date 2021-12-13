import datetime
import unittest

import urbanairship as ua


class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.start_hour = 7
        self.end_hour = 15
        self.start_date = datetime.datetime(2021, 1, 15)
        self.end_date = datetime.datetime(2021, 4, 15)
        self.days_of_week = ["friday", "saturday", "sunday"]

    def test_scheduled_time(self):
        d = datetime.datetime(2013, 1, 1, 12, 56)
        self.assertEqual(
            ua.scheduled_time(d), {"scheduled_time": "2013-01-01T12:56:00"}
        )

    def test_local_scheduled_time(self):
        d = datetime.datetime(2015, 1, 1, 12, 56)
        self.assertEqual(
            ua.local_scheduled_time(d), {"local_scheduled_time": "2015-01-01T12:56:00"}
        )

    def test_best_time(self):
        d = datetime.datetime(2018, 10, 8)
        self.assertEqual(ua.best_time(d), {"best_time": {"send_date": "2018-10-08"}})

    def test_schedule_exclusion(self):
        self.assertEqual(
            ua.schedule_exclusion(
                start_hour=self.start_hour,
                end_hour=self.end_hour,
                start_date=self.start_date,
                end_date=self.end_date,
                days_of_week=self.days_of_week,
            ),
            {
                "hour_range": "7-15",
                "date_range": "2021-01-15T00:00:00/2021-04-15T00:00:00",
                "days_of_week": ["friday", "saturday", "sunday"],
            },
        )

    def test_schedule_exclusion_raises_bad_hour(self):
        with self.assertRaises(ValueError):
            ua.schedule_exclusion(
                start_hour=self.start_hour,
                end_hour=25,
                start_date=self.start_date,
                end_date=self.end_date,
                days_of_week=self.days_of_week,
            )

    def test_schedule_exclusion_raises_bad_date(self):
        with self.assertRaises(ValueError):
            ua.schedule_exclusion(
                start_hour=self.start_hour,
                end_hour=self.end_hour,
                start_date=self.start_date,
                end_date="not_a_datetime",
                days_of_week=self.days_of_week,
            )

    def test_schedule_exclusion_raises_bad_day_of_week(self):
        with self.assertRaises(ValueError):
            ua.schedule_exclusion(
                start_hour=self.start_hour,
                end_hour=self.end_hour,
                start_date=self.start_date,
                end_date=self.end_date,
                days_of_week=["fakesday"],
            )

    def test_recurring_schedule_standard(self):
        self.assertEqual(
            ua.recurring_schedule(
                count=1,
                type="daily",
                end_time=datetime.datetime(2030, 1, 15, 12, 0, 0),
                paused=False,
                exclusions=[
                    ua.schedule_exclusion(
                        start_hour=self.start_hour,
                        end_hour=self.end_hour,
                        start_date=self.start_date,
                        end_date=self.end_date,
                        days_of_week=self.days_of_week,
                    )
                ],
            ),
            {
                "recurring": {
                    "cadence": {"type": "daily", "count": 1},
                    "end_time": "2030-01-15T12:00:00",
                    "exclusions": [
                        {
                            "hour_range": "7-15",
                            "date_range": "2021-01-15T00:00:00/2021-04-15T00:00:00",
                            "days_of_week": ["friday", "saturday", "sunday"],
                        }
                    ],
                    "paused": False,
                }
            },
        )

    def test_recurring_schedule_weekly(self):
        self.assertEqual(
            ua.recurring_schedule(
                count=1,
                type="weekly",
                days_of_week=["monday", "wednesday", "friday"],
                end_time=datetime.datetime(2030, 1, 15, 12, 0, 0),
                paused=False,
                exclusions=[
                    ua.schedule_exclusion(
                        start_hour=self.start_hour,
                        end_hour=self.end_hour,
                        start_date=self.start_date,
                        end_date=self.end_date,
                        days_of_week=self.days_of_week,
                    )
                ],
            ),
            {
                "recurring": {
                    "cadence": {
                        "type": "weekly",
                        "count": 1,
                        "days_of_week": ["monday", "wednesday", "friday"],
                    },
                    "end_time": "2030-01-15T12:00:00",
                    "exclusions": [
                        {
                            "hour_range": "7-15",
                            "date_range": "2021-01-15T00:00:00/2021-04-15T00:00:00",
                            "days_of_week": ["friday", "saturday", "sunday"],
                        }
                    ],
                    "paused": False,
                }
            },
        )

    def test_recurring_schedule_raises_bad_day(self):
        with self.assertRaises(ValueError):
            ua.recurring_schedule(count=1, type="weekly", days_of_week=["fakesday"])

    def test_recurring_schedule_raises_bad_type(self):
        with self.assertRaises(ValueError):
            ua.recurring_schedule(count=1, type="fake_type")
