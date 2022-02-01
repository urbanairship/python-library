import json
import logging
from typing import Optional, Dict, TypeVar

from requests import Response

from urbanairship import common, Airship

logger = logging.getLogger("urbanairship")


class Segment(object):
    url: Optional[str] = None
    id: Optional[str] = None
    display_name: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    criteria: Optional[str] = None
    data: Optional[Dict] = None

    def create(self, airship: Airship) -> Response:
        """Create a Segment object and return it."""

        url = airship.urls.get("segments_url")

        body = json.dumps(
            {"display_name": self.display_name, "criteria": self.criteria}
        )
        response = airship._request(method="POST", body=body, url=url, version=3)
        logger.info("Successful segment creation: {0}".format(self.display_name))

        payload = response.json()
        seg_id = payload.get("segment_id")

        self.id = seg_id
        self.from_id(airship, seg_id)

        return response

    @classmethod
    def from_id(cls, airship: Airship, seg_id: str):
        """Retrieve a segment based on the provided ID."""

        url = airship.urls.get("segments_url") + seg_id
        response = airship._request(method="GET", body=None, url=url, version=3)

        payload = response.json()
        cls.id = seg_id
        cls.from_payload(payload)

        return response

    @classmethod
    def from_payload(cls, payload: Dict):
        """Create segment based on results from a SegmentList iterator."""

        for key in payload:
            setattr(cls, key, payload[key])

        return cls

    def update(self, airship: Airship) -> Response:
        """Updates the segment associated with data in the current object."""

        data = {}
        data["display_name"] = self.display_name
        data["criteria"] = self.criteria

        url = f'{airship.urls.get("segments_url")}{self.id}'
        body = json.dumps(data)
        response = airship._request(method="PUT", body=body, url=url, version=3)
        logger.info("Successful segment update: '{0}'".format(self.display_name))

        return response

    def delete(self, airship: Airship) -> Response:
        url = f'{airship.urls.get("segments_url")}{self.id}'
        res = airship._request(method="DELETE", body=None, url=url, version=3)
        logger.info("Successful segment deletion: '{0}'".format(self.display_name))
        return res


class SegmentList(common.IteratorParent):
    """Retrieves a list of segments

    :keyword limit: Number of segments to fetch

    """

    next_url: Optional[str] = None
    data_attribute: str = "segments"

    def __init__(self, airship: Airship, limit: Optional[int] = None):
        self.next_url = airship.urls.get("segments_url")
        params = {"limit": limit} if limit else {}
        super(SegmentList, self).__init__(airship, params)
