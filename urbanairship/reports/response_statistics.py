from urbanairship import common
from datetime import datetime

class IndividualResponseStatistics(object):
    def __init__(self, airship):
        self.airship = airship

    def get(self, push_id):
        url = common.INDIVIDUAL_RESPONSE_STATS_URL + push_id
        response = self.airship._request('GET', None, url, version=3)
        return response.json()

class ResponseListing(object):
    def __init__(self, airship):
        self.airship = airship
        self.url = common.RESPONSE_LISTING_URL

    def get(self, start_date, end_date, limit=None, start_id=None):
        if not start_date or not end_date:
            raise TypeError('start_date and end_date cannot be empty')
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise ValueError(
                'start and end date must both be datetime objects')
        params = {
            'start': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': end_date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        if limit is not None:
            params['limit'] = limit
        if start_id is not None:
            params['start_id'] = start_id

        response = self.airship._request('GET', None, self.url, version=3, params=params)
        return response.json()
