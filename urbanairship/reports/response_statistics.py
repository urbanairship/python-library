from urbanairship import common

class IndividualResponseStats(object):
    def __init__(self, airship):
        self.airship = airship

    def get(self, push_id):
        url = common.REPORTS_URL + 'responses/'+ push_id
        response = self.airship._request('GET', None, url, version=3)
        return response.json()
