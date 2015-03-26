import json
import logging

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

        #TODO: Verify that start and end are both valid dates

        url = common.REPORTS_URL + 'perpush/series/{0}?precision={1}&start={2}&end{3}'.format(push_id, precision, start, end)
        response = airship._request('GET', None, url, version=3)

        return response.json()