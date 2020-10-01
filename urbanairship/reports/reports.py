from urbanairship import common
from datetime import datetime


class IndividualResponseStats(object):
    def __init__(self, airship):
        self.airship = airship

    def get(self, push_id):
        url = self.airship.urls.get('reports_url') + 'responses/' + push_id
        response = self.airship.request('GET', None, url, version=3)
        payload = response.json()
        return common.IteratorDataObj.from_payload(payload)


class ResponseList(common.IteratorParent):
    next_url = None
    data_attribute = 'pushes'

    def __init__(
            self, airship, start_date, end_date, limit=None, start_id=None
    ):
        if not airship or not start_date or not end_date:
            raise TypeError('airship, start_date, & end_date cannot be empty')
        if not isinstance(start_date, datetime) or not \
                isinstance(end_date, datetime):
            raise TypeError('start_date and end_date must be datetime objects')
        params = {
            'start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end': end_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        if limit:
            params['limit'] = limit
        if start_id:
            params['start_id'] = start_id
        self.next_url = airship.urls.get('reports_url') + 'responses/list'
        super(ResponseList, self).__init__(airship, params)


class DevicesReport(object):
    def __init__(self, airship):
        self.airship = airship

    def get(self, date):
        if not date:
            raise TypeError("date cannot be empty")
        if not isinstance(date, datetime):
            raise ValueError(
                'date must be a datetime object')
        url = self.airship.urls.get('reports_url') + 'devices/'
        params = {
            'date': date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        response = self.airship._request(
            'GET', None, url, version=3, params=params
        )
        return response.json()


class ReportsList(common.IteratorParent):
    next_url = None
    data_attribute = None

    def __init__(self, airship, start_date, end_date, precision):
        if not airship or not start_date or not end_date or not precision:
            raise TypeError('None of the function parameters can be empty')

        if not isinstance(start_date, datetime) or not \
                isinstance(end_date, datetime):
            raise TypeError('start_date and end_date must be datetime objects')

        if precision not in ['HOURLY', 'DAILY', 'MONTHLY']:
            raise ValueError(
                "Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'"
            )

        base_url = airship.urls.get('reports_url')

        if self.data_attribute == 'optins':
            self.next_url = base_url + 'optins/'
        elif self.data_attribute == 'optouts':
            self.next_url = base_url + 'optouts/'
        elif self.data_attribute == 'sends':
            self.next_url = base_url + 'sends/'
        elif self.data_attribute == 'responses':
            self.next_url = base_url + 'responses/'
        elif self.data_attribute == 'opens':
            self.next_url = base_url + 'opens/'
        elif self.data_attribute == 'timeinapp':
            self.next_url = base_url + 'timeinapp/'
        elif self.data_attribute == 'events':
            self.next_url = base_url + 'events/'

        params = {
            'start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end': end_date.strftime('%Y-%m-%d %H:%M:%S'),
            'precision': precision
        }

        super(ReportsList, self).__init__(airship, params)


class OptInList(ReportsList):
    data_attribute = 'optins'


class OptOutList(ReportsList):
    data_attribute = 'optouts'


class PushList(ReportsList):
    data_attribute = 'sends'


class ResponseReportList(ReportsList):
    data_attribute = 'responses'


class AppOpensList(ReportsList):
    data_attribute = 'opens'


class TimeInAppList(ReportsList):
    data_attribute = 'timeinapp'
    

class CustomEventsList(ReportsList):
    data_attribute = 'events'
