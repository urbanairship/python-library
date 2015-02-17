import json
import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')


class Segment(object):
    _airship = None
    url = None

    id = None
    display_name = None
    creation_date = None
    modification_date = None
    criteria = None
    data = None

    @classmethod
    def from_payload(cls, payload):
        """Create segment based on results from a SegmentList iterator.
        """
        obj = cls()
        for key in payload:
            setattr(obj, key, payload[key])
        return obj

    @classmethod
    def from_id(cls, airship, seg_id):
        """Retrieve a segment based on the provided ID
        """
        cls._airship = airship
        url = common.SEGMENTS_URL + seg_id
        response = airship._request('GET', None, url, version=3)
        payload = response.json()
        seg = cls.from_payload(payload)
        seg.id = seg_id
        return seg

    def create(self, airship, name, criteria):
        """Create a Segment object and return it
        """

        url = common.SEGMENTS_URL
        data = {
            'display_name': name,
            'criteria': criteria
        }

        body = json.dumps(data)
        response = airship._request('POST', body, url, version=3)
        logger.info("Successful segment creation: '{}'".format(name))
        seg_url = response.headers['location']
        seg_id = seg_url.split(url)[1]

        created_segment = self.from_id(airship, seg_id)
        created_segment.id = seg_id
        return created_segment

    def update(self):
        """Updates the segment associated with the data in the current object
        """
        url = common.SEGMENTS_URL + self.id
        data = {}

        if self.display_name is not None:
            data['display_name'] = self.display_name
        if self.criteria is not None:
            data['criteria'] = self.criteria

        body = json.dumps(data)
        response = self._airship._request('PUT', body, url, version=3)
        logger.info(
            "Successful segment update: '{}'".format(self.display_name))
        return response

    def delete(self):
        url = common.SEGMENTS_URL + self.id
        res = self._airship._request('DELETE', None, url, version=3)
        logger.info(
            "Successful segment deletion: '{}'".format(self.display_name))
        return res


class SegmentList(object):
    """Retrieves a list of segments

        :ivar limit: Number of segments to fetch
    """

    start_url = None
    next_url = None
    airship = None
    data = None
    limit = None

    def __init__(self, airship, limit=None):
        self._airship = airship
        self.start_url = common.SEGMENTS_URL
        self.next_url = self.start_url
        self._token_iter = iter(())
        if limit is not None:
            self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return Segment.from_payload(next(self._token_iter))
        except StopIteration:
            self._fetch_next_page()
            return Segment.from_payload(next(self._token_iter))

    def next(self):
        """ Necessary for iteration to work with Python 2.*
        """
        return self.__next__()

    def _fetch_next_page(self):
        if self.next_url:
            self._load_page(self.next_url)
            self.next_url = self._page.get('next_page')

    def _load_page(self, url):
        if self.limit is not None:
            params = {'limit': self.limit}
        else:
            params = None

        response = self._airship._request('GET', None, url, version=3,
                                          params=params)
        self._page = page = response.json()
        self._token_iter = iter(page['segments'])