from urbanairship import common
import json
import logging

logger = logging.getLogger('urbanairship')


class Segment(object):
    """Change the definition for a segment

    """

    _airship = None
    url = None
    data = None
    segment_name = None


    def __init__(self, airship, segment_name, data):
        self._airship = airship
        self.url = common.SEGMENTS_URL
        self.data = data
        self.segment_name = segment_name

    def create(self):
        body = json.dumps(self.data)
        response = self._airship._request('POST', body, self.url, version=3)
        logger.info(("Successful segment creation: '{}'").format(self.segment_name))

    def update(self):
        body = json.dumps(self.data)
        response = self._airship._request('PUT', body, self.url, version=3)
        logger.info(("Successful segment update: '{}'").format(self.segment_name))

    def set_criteria(self, criteria=None):
        """Adds criteria to a segment

        """

        if criteria is not None:
            self.data['criteria'] = criteria

class SegmentList(object):
    """Retrieves a list of segments
        :ivar limit: Number of segments to fetch
    """
    url = None
    next_url = None
    airship = None
    data = None

    def __init__(self, airship):
        self._airship = airship
        self.url = common.SEGMENTS_URL
        self.next_url = self.url
        self._token_iter = iter(())

    def __iter__(self):
        return self

    def __next__(self):
        return {'test': 'something'}

    def listSegments(self, limit=None):
        params = {'limit': limit} if limit is not None else {}
        response = self._airship._request('GET', None, self.url, version=3, params=params)
        logger.info("Retrieving segment list successful")
        return response.json()
