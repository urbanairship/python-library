from datetime import datetime
from typing import Dict, Any, Optional

from urbanairship import common, Airship

DATE_FORMAT_STR: str = "%Y-%m-%d %H:%M:%S"


class IndividualResponseStats(object):
    """Returns detailed reports information about a specific push notification."""

    def __init__(self, airship: Airship) -> None:
        self.airship = airship

    def get(self, push_id: str) -> common.IteratorDataObj:
        url = self.airship.urls.get("reports_url") + "responses/" + push_id
        response = self.airship.request(method="GET", body="", url=url, version=3)
        payload = response.json()
        return common.IteratorDataObj.from_payload(payload)


class ResponseList(common.IteratorParent):
    """Get a listing of all pushes, plus basic response information, in a given
    timeframe. Start and end date times are required parameters.
    """

    next_url: Optional[str] = None
    data_attribute: str = "pushes"

    def __init__(
        self,
        airship: Airship,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[str] = None,
        start_id: Optional[str] = None,
    ):
        if not airship or not start_date or not end_date:
            raise TypeError("airship, start_date, & end_date cannot be empty")
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError("start_date and end_date must be datetime objects")
        params = {
            "start": start_date.strftime(DATE_FORMAT_STR),
            "end": end_date.strftime(DATE_FORMAT_STR),
        }
        if limit:
            params["limit"] = limit
        if start_id:
            params["start_id"] = start_id
        self.next_url = airship.urls.get("reports_url") + "responses/list"
        super(ResponseList, self).__init__(airship, params)


class DevicesReport(object):
    """Returns a project's opted-in and installed device counts broken out by device
    type as a daily snapshot. This endpoint returns the same data that populates the
    Devices Report on the web dashboard."""

    def __init__(self, airship: Airship):
        self.airship = airship

    def get(self, date: datetime):
        if not date:
            raise TypeError("date cannot be empty")
        if not isinstance(date, datetime):
            raise ValueError("date must be a datetime object")
        url = self.airship.urls.get("reports_url") + "devices/"
        params = {"date": date.strftime(DATE_FORMAT_STR)}
        response = self.airship._request(
            method="GET", body="", url=url, version=3, params=params
        )
        return response.json()


class ReportsList(common.IteratorParent):
    """Parent class for reports"""

    next_url: Optional[str] = None
    data_attribute: Optional[str] = None

    def __init__(
        self, airship: Airship, start_date: datetime, end_date: datetime, precision: str
    ):
        if not airship or not start_date or not end_date or not precision:
            raise TypeError("None of the function parameters can be empty")

        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError("start_date and end_date must be datetime objects")

        if precision not in ["HOURLY", "DAILY", "MONTHLY"]:
            raise ValueError("Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'")

        base_url = airship.urls.get("reports_url")

        params = {
            "start": start_date.strftime(DATE_FORMAT_STR),
            "end": end_date.strftime(DATE_FORMAT_STR),
            "precision": precision,
        }

        if self.data_attribute == "optins":
            self.next_url = base_url + "optins/"
        elif self.data_attribute == "optouts":
            self.next_url = base_url + "optouts/"
        elif self.data_attribute == "sends":
            self.next_url = base_url + "sends/"
        elif self.data_attribute == "responses":
            self.next_url = base_url + "responses/"
        elif self.data_attribute == "opens":
            self.next_url = base_url + "opens/"
        elif self.data_attribute == "timeinapp":
            self.next_url = base_url + "timeinapp/"
        elif self.data_attribute == "events":
            self.next_url = base_url + "events/"
        elif self.data_attribute == "total_counts":
            self.next_url = base_url + "web/interaction/"
            params["app_key"] = airship.key

        super(ReportsList, self).__init__(airship, params)


class OptInList(ReportsList):
    """Get the number of opted-in Push users who access the app within the specified
    time period.
    """

    data_attribute = "optins"


class OptOutList(ReportsList):
    """Get the number of opted-out Push users who access the app within the
    specified time period
    """

    data_attribute = "optouts"


class PushList(ReportsList):
    """Get the number of pushes you have sent within a specified time period."""

    data_attribute = "sends"


class ResponseReportList(ReportsList):
    """Get the number of direct and influenced opens of your app."""

    data_attribute = "responses"


class AppOpensList(ReportsList):
    """Get the number of users who have opened your app within the specified time period."""

    data_attribute = "opens"


class TimeInAppList(ReportsList):
    """Get the average amount of time users have spent in your app within the specified
    time period.
    """

    data_attribute = "timeinapp"


class CustomEventsList(ReportsList):
    """Get a summary of custom event counts and values, by custom event, within the
    specified time period.
    """

    data_attribute = "events"


class WebResponseReport(ReportsList):
    """Get the web interaction data for the given app key. Accepts a required start
    time and optional end time and precision parameters.
    """

    data_attribute = "total_counts"
