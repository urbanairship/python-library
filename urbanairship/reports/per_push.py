import json
import logging
from datetime import datetime
from urbanairship import common


class Detail(object):
    def get_single(self, airship, push_id):
        response = airship._request('GET', None, common.REPORTS_URL +
                                    'perpush/detail/' + push_id, version=3)
        return response.json()

    def get_batch(self, airship, push_ids):
        data = {}
        data['push_ids'] = push_ids
        body = json.dumps(data)

        response = airship._request('POST', body, common.REPORTS_URL +
                            'perpush/detail/', version=3)
        return response.json()



class Series(object):
    def get(self, airship, push_id):

        url = common.REPORTS_URL + 'perpush/series/{0}'.format(push_id)
        response = airship._request('GET', None, url, version=3)
        return response.json()

    def get_with_precision(self, airship, push_id, precision):
        if precision not in ['HOURLY', 'DAILY', 'MONTHLY']:
            raise ValueError("Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'")

        url = common.REPORTS_URL + 'perpush/series/{0}?precision={1}'.format(push_id, precision)

        response = airship._request('GET', None, url, version=3)
        return response.json()

    def get_with_precision_and_range(self, airship, push_id, precision, start, end):
        if precision not in ['HOURLY', 'DAILY', 'MONTHLY']:
            raise ValueError("Precision must be 'HOURLY', 'DAILY', or 'MONTHLY'")

        newstart = None
        newend = None

        for format in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
            try:
                newstart = datetime.strptime(start, format)
            except ValueError:
                pass

        for format in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
            try:
                newend = datetime.strptime(end, format)
            except ValueError:
                pass

        if newstart is None or newend is None:
            raise ValueError("'start' and 'end' date must be in the form: YYYY-MM-DD H:M:S or YY-MM-DD")

        url = common.REPORTS_URL + 'perpush/series/{0}?precision={1}&start={2}&end{3}'.format(push_id, precision, start, end)
        response = airship._request('GET', None, url, version=3)

        return response.json()