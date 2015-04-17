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

    def create(self, airship):
        """Create a Segment object and return it."""

        url = common.SEGMENTS_URL

        body = json.dumps(
            {
                'display_name': self.display_name,
                'criteria': self.criteria
            }
        )
        response = airship._request(
            method='POST',
            body=body,
            url=url,
            version=3
        )
        logger.info(
            'Successful segment creation: {0}'.format(self.display_name)
        )

        seg_url = response.headers['location']
        seg_id = seg_url.split(url)[1]

        self.id = seg_id
        self.from_id(airship, seg_id)

        return response

    @classmethod
    def from_id(cls, airship, seg_id):
        """Retrieve a segment based on the provided ID."""

        url = common.SEGMENTS_URL + seg_id
        response = airship._request(
            method='GET',
            body=None,
            url=url,
            version=3
        )

        payload = response.json()
        cls.id = seg_id
        cls.from_payload(payload)

        return response

    @classmethod
    def from_payload(cls, payload):
        """Create segment based on results from a SegmentList iterator."""

        for key in payload:
            setattr(cls, key, payload[key])

        return cls

    def update(self, airship):
        """Updates the segment associated with data in the current object."""

        data = {}
        data['display_name'] = self.display_name
        data['criteria'] = self.criteria

        url = common.SEGMENTS_URL + self.id
        body = json.dumps(data)
        response = airship._request(
            method='PUT',
            body=body,
            url=url,
            version=3
        )
        logger.info(
            "Successful segment update: '{0}'".format(self.display_name))

        return response

    def delete(self, airship):
        url = common.SEGMENTS_URL + self.id
        res = airship._request(
            method='DELETE',
            body=None,
            url=url,
            version=3
        )
        logger.info(
            "Successful segment deletion: '{0}'".format(self.display_name))
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
        """ Necessary for iteration to work with Python 2.*."""
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

        response = self._airship._request(
            method='GET',
            body=None,
            url=url,
            version=3,
            params=params
        )
        self._page = page = response.json()
        self._token_iter = iter(page['segments'])