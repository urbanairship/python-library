import json
import logging
from datetime import datetime
from urbanairship import common


class PerPushDetail(object):
    airship = None

    def __init__(self, airship):
        self.airship = airship

    def get_single(self, push_id):
        if not push_id:
            raise ValueError('push_id cannot be empty')

        url = '{0}perpush/detail/{1}'.format(common.REPORTS_URL, push_id)
        response = self.airship._request('GET', None, url, version=3)

        return response.json()

    def get_batch(self, push_ids):
        if not push_ids or push_ids is []:
            raise ValueError('push_ids cannot be empty')
        if not isinstance(push_ids, list):
            raise TypeError('push_ids must be a list')
        if len(push_ids) > 100:
            raise ValueError('push_ids can not contain more than 100 IDs')

        data = {}
        data['push_ids'] = push_ids
        body = json.dumps(data)
        url = '{0}perpush/detail/'.format(common.REPORTS_URL)
        response = self.airship._request('POST', body, url, version=3)

        return response.json()


class PerPushSeries(object):
    airship = None

    def __init__(self, airship):
        self.airship = airship

    def get(self, push_id):
        if not push_id:
            raise TypeError('push_id cannot be empty')

        url = '{0}perpush/series/{1}'.format(common.REPORTS_URL, push_id)
        response = self.airship._request('GET', None, url, version=3)
        return response.json()

    def get_with_precision(self, push_id, precision):
        if not push_id:
            raise TypeError('push_id cannot be empty')
        if precision not in ['HOURLY', 'DAILY', 'MONTHLY']:
            raise ValueError(
                "Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'"
            )

        url = '{0}perpush/series/{1}'.format(common.REPORTS_URL, push_id)

        params = {'precision': precision}
        response = self.airship._request(
            'GET',
            None,
            url,
            version=3,
            params=params
        )

        return response.json()

    def get_with_precision_and_range(self, push_id, precision, start, end):
        if not push_id:
            raise TypeError('push_id cannot be empty')
        if precision not in ['HOURLY', 'DAILY', 'MONTHLY']:
            raise ValueError(
                "Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'")
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise ValueError(
                'start and end date must both be datetime objects'
            )

        url = '{0}perpush/series/{1}'.format(common.REPORTS_URL, push_id)
        params = {
            'precision': precision,
            'start': start.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': end.strftime('%Y-%m-%dT%H:%M:%S')
        }

        response = self.airship._request(
            'GET',
            None,
            url,
            version=3,
            params=params
        )

        return response.json()
