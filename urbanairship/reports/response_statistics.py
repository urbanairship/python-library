from urbanairship import common

class IndividualResponseStatistics(object):
    def __init__(self, airship):
        self.airship = airship

    def get(self, push_id):
        url = common.INDIVIDUAL_RESPONSE_STATS_URL + push_id
        response = self.airship._request('GET', None, url, version=3)
        return response.json()