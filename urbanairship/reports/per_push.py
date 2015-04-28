import json
import logging
from datetime import datetime
from urbanairship import common


class Detail(object):
    self.airship = None

    def __init__(self, airship):
        self.airship = airship

    def get_single(self, push_id):
        if not push_id:
            raise ValueError("'push_id' cannot be empty")

        if not isinstance(push_id, str):
            raise TypeError("'push_id' must be a string")
        response = self.airship._request('GET', None, common.REPORTS_URL +
                                         'perpush/detail/' + push_id,
                                         version=3)
        return response.json()

    def get_batch(self, push_ids):
        if not push_ids or push_ids is []:
            raise ValueError("'push_ids' cannot be empty")
        if not isinstance(push_ids, list):
            raise TypeError("'push_ids' must be a list")
        if len(push_ids) > 100:
            raise ValueError("'push_ids' can not contain more than 100 IDs")

        data = {}
        data['push_ids'] = push_ids
        body = json.dumps(data)

        response = self.airship._request('POST', body, common.REPORTS_URL +
                                         'perpush/detail/', version=3)
        return response.json()


class Series(object):
    self.airship = None

    def init(self, airship):
        self.airship = airship

    def get(self, push_id):
        if not isinstance(push_id, str):
            raise TypeError("'push_id' must be a string")

        url = common.REPORTS_URL + 'perpush/series/{0}'.format(push_id)
        response = self.airship._request('GET', None, url, version=3)
        return response.json()

    def get_with_precision(self, push_id, precision):
        if not isinstance(push_id, str):
            raise TypeError("'push_id' must be a string")
        if precision not in ['HOURLY', 'DAILY', 'MONTHLY']:
            raise ValueError(
                "Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'")

        url = common.REPORTS_URL + 'perpush/series/{0}?precision={1}'.format(
            push_id, precision)

        response = self.airship._request('GET', None, url, version=3)
        return response.json()

    def get_with_precision_and_range(self, push_id, precision, start,
                                     end):
        if not isinstance(push_id, str):
            raise TypeError("'push_id' must be a string")
        if precision not in ['HOURLY', 'DAILY', 'MONTHLY']:
            raise ValueError(
                "Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'")

        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise ValueError(
                'start and end date must both be datetime objects'
            )

        url = common.REPORTS_URL + (
            'perpush/series/{0}?precision={1}&start={2}&end{3}'
        ).format(push_id, precision, str(start), str(end))

        response = self.airship._request('GET', None, url, version=3)

        return response.json()