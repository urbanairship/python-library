from datetime import datetime

from typing import Any, List, Dict, Optional, Type

from urbanairship import common, Airship
from urbanairship.push.core import ScheduledPush


VALID_DAYS: List[str] = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

VALID_RECURRING_TYPES: List[str] = ["hourly", "daily", "weekly", "monthly", "yearly"]
DT_FORMAT_STR: str = "%Y-%m-%dT%H:%M:%S"


class ScheduledList(common.IteratorParent):
    """
    Iterator for listing all scheduled messages.

    :keyword limit: Number of entries to fetch in a paginated request.

    :returns: Each ``next`` returns a :py:class:`ScheduledPush` object.
    """

    next_url: Optional[str] = None
    data_attribute: str = "schedules"
    id_key: str = "url"
    instance_class: Type[ScheduledPush] = ScheduledPush

    def __init__(self, airship: Airship, limit: int = None) -> None:
        self.next_url = airship.urls.get("schedules_url")
        params = {"limit": limit} if limit else {}
        super(ScheduledList, self).__init__(airship, params)


def scheduled_time(timestamp: datetime) -> Dict[str, Any]:
    """Specify a time for the delivery of this push.

    :param timestamp: A ``datetime.datetime`` object.

    """

    return {"scheduled_time": timestamp.strftime(DT_FORMAT_STR)}


def local_scheduled_time(timestamp: datetime) -> Dict[str, Any]:
    """Specify a time for the delivery of this push in device local time.

    :param timestamp: A ``datetime.datetime`` object.

    """

    return {"local_scheduled_time": timestamp.strftime(DT_FORMAT_STR)}


def best_time(timestamp: datetime) -> Dict[str, Any]:
    """Specify a date to send the push at the best time per-device.
    Only YYYY_MM_DD are needed. Hour/minute/second information is discarded.

    :param timestamp: A ``datetime.datetime`` object.
    """

    return {"best_time": {"send_date": timestamp.strftime("%Y-%m-%d")}}


def schedule_exclusion(
    start_hour: Optional[int] = None,
    end_hour: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    days_of_week: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Date-time ranges when messages are not sent.
    at least one of start_hour and end_hour, start_date and end_date, or days_of_week
    must be included. All dates and times are inclusive.

    :param start_hour: Optional. An integer 0-23 representing the UTC hour to start
        exclusion.
    :param end_hour: Optional. An integer 0-23 representing the UTC hour to stop
        exclusion. Must be included if start_hour is used.
    :param start_date: Optional. A datetime.datetime object representing the UTC date
        to start exclusion. Hour/minute/seconds will be excluded.
    :param start_date: Optional. A datetime.datetime object representing the UTC date
        to stop exclusion. Hour/minute/seconds will be excluded. Must be included if
        start_date is used.
    :param days_of_week: Optional. A list of the days of the week to exclude on.
        Possible values: monday, tuesday, wednesday, thursday, friday, saturday, sunday
    """

    exclusion: Dict[str, Any] = {}

    if isinstance(start_hour, int) and isinstance(end_hour, int):
        if not all([0 < start_hour < 24, 0 < end_hour < 24]):
            raise ValueError("start_hour and end_hour must be int 0-23")
        else:
            exclusion["hour_range"] = "{}-{}".format(start_hour, end_hour)

    if isinstance(start_date, datetime) and isinstance(end_date, datetime):
        exclusion["date_range"] = "{}/{}".format(
            start_date.strftime(DT_FORMAT_STR),
            end_date.strftime(DT_FORMAT_STR),
        )
    else:
        raise ValueError("start_date and end_date must be datetime.datetime")

    if days_of_week:
        for day in days_of_week:
            if day not in VALID_DAYS:
                raise ValueError("days_of_week must be {}".format(VALID_DAYS))

        exclusion["days_of_week"] = days_of_week

    return exclusion


def recurring_schedule(
    count: int,
    type: str,
    end_time: Optional[datetime] = None,
    days_of_week: Optional[List[str]] = None,
    exclusions: Optional[List[Dict[str, Any]]] = None,
    paused: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    Sets the cadence, end time, and excluded times for a recurring scheduled
    message.

    :param count: Required. The frequency of messaging corresponding to the type.
        For example, a count of 2 results in a message every 2 hours, days, weeks,
        months, etc based on the type.
    :param type: Required. The unit of measurement for the cadence. Possible
        values: hourly, daily, monthly, yearly.
    :param days_of_week: Required when type is weekly. The days of the week on which
        Airship can send your message.
    :param end_time: Optional. A datetime.datetime object representing when the
        scheduled send will end and stop sending messages.
    :param exclusions: Optional. A list of urbanaiship.schedule_exclusion defining
        times in which Airship will not send your message.
    :param paused: Optional. A boolean value respesnting the paused state of the
        scheduled message.
    """
    if days_of_week is not None:
        for day in days_of_week:
            if day not in VALID_DAYS:
                raise ValueError("days of week can only include {}".format(VALID_DAYS))

    if type not in VALID_RECURRING_TYPES:
        raise ValueError("type must be one of {}".format(VALID_RECURRING_TYPES))

    cadence: Dict[str, Any] = {"type": type, "count": count}

    if type == "weekly":
        cadence["days_of_week"] = days_of_week

    recurring: Dict[str, Any] = {"cadence": cadence}

    if end_time:
        recurring["end_time"] = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    if exclusions:
        recurring["exclusions"] = exclusions
    if paused is not None:
        recurring["paused"] = paused

    return {"recurring": recurring}
