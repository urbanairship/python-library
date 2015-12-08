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


class SegmentList(common.IteratorParent):
    """Retrieves a list of segments

        :ivar limit: Number of segments to fetch

    """
    next_url = common.SEGMENTS_URL
    data_attribute = 'segments'

    def __init__(self, airship, limit=None):
        params = {'limit': limit} if limit else {}
        super(SegmentList, self).__init__(airship, params)
