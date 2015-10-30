from urbanairship import common
from datetime import datetime
from abc import abstractmethod


class IndividualResponseStats(object):
    def __init__(self, airship):
        self.airship = airship

    def get(self, push_id):
        url = common.REPORTS_URL + 'responses/' + push_id
        response = self.airship.request('GET', None, url, version=3)
        payload = response.json()
        return common.IteratorDataObj.from_payload(payload)


class ResponseList(common.IteratorParent):
    next_url = common.REPORTS_URL + 'responses/list'
    data_attribute = 'pushes'

    def __init__(self, airship, start_date, end_date, limit=None, start_id=None):
        if not airship or not start_date or not end_date:
            raise TypeError('airship, start_date, and end_date cannot be empty')
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError('start_date and end_date must be datetime objects')
        params = {
            'start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end': end_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        if limit:
            params['limit'] = limit
        if start_id:
            params['start_id'] = start_id
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
        url = common.REPORTS_URL + 'devices/'
        params = {
            'date': date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        response = self.airship._request('GET', None, url, version=3, params=params)
        return response.json()


class OptInList(common.IteratorParent):
    next_url = common.REPORTS_URL + 'optins/'
    data_attribute = 'optins'

    def __init__(self, airship, start_date, end_date, precision):
        if not airship or not start_date or not end_date or not precision:
            raise TypeError('None of the function parameters can be empty')
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise TypeError('start_date and end_date must be datetime objects')
        if precision not in ['HOURLY', 'DAILY', 'MONTHLY']:
            raise ValueError("Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'")
        params = {
            'start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end': end_date.strftime('%Y-%m-%d %H:%M:%S'),
            'precision': precision
        }
        super(OptInList, self).__init__(airship, params)


class OptOutList(OptInList):
    next_url = common.REPORTS_URL + 'optouts/'
    data_attribute = 'optouts'


class PushList(OptInList):
    next_url = common.REPORTS_URL + 'sends/'
    data_attribute = 'sends'


class ResponseReportList(OptInList):
    next_url = common.REPORTS_URL + 'responses/'
    data_attribute = 'responses'


class AppOpensList(OptInList):
    next_url = common.REPORTS_URL + 'opens/'
    data_attribute = 'opens'


class TimeInAppList(OptInList):
    next_url = common.REPORTS_URL + 'timeinapp/'
    data_attribute = 'timeinapp'
