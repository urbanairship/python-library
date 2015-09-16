from urbanairship import common
from datetime import datetime
from abc import abstractmethod


class IndividualResponseStats(object):
    """Information object for an individual push response

    :ivar push_uuid: Push ID
    :ivar push_time: UTC date and time of the push
    :ivar push_type: Describes the push operation, which is often comparable to
        the audience selection, e.g. BROADCAST_PUSH.
    :ivar direct_responses: Number of direct responses
    :ivar sends: Number of sends
    :ivar group_id: Group ID

    """
    push_uuid = None
    push_time = None
    push_type = None
    direct_responses = None
    sends = None
    group_id = None

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
        params = {
            'start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end': end_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        if limit is not None:
            params['limit'] = limit
        if start_id is not None:
            params['start_id'] = start_id
        if len(params) == 0:
            params = None
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
