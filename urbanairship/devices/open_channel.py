import datetime
import json
import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')


class OpenChannel(object):
    channel_id = None
    address = None
    open_platform = None
    identifiers = None
    opt_in = None
    installed = None
    created = None
    last_registration = None
    tags = None

    def __init__(self, airship):
        self.airship = airship

    def create(self, set_tags=None):
        """Create this OpenChannel object with the API."""

        if self.tags and set_tags is None:
            raise ValueError(
                'set_tags may not be None when tags present on OpenChannel.'
            )

        if not self.address:
            raise ValueError('Must set address before creation.')

        if not self.open_platform:
            raise ValueError('Must set open_platform before creation.')

        if not self.opt_in:
            raise ValueError('Must set opt_in before creation.')

        url = common.OPEN_CHANNEL_URL

        channel_data = {
            'type': 'open',
            'address': self.address,
            'opt_in': self.opt_in,
            'open': {'open_platform_name': self.open_platform}
        }

        if self.tags:
            channel_data['tags'] = self.tags
            channel_data['set_tags'] = set_tags
        if self.identifiers:
            channel_data['open']['identifiers'] = self.identifiers

        body = json.dumps({'channel': channel_data})
        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            version=3
        )

        self.channel_id = response.json().get('channel_id')

        logger.info(
            'Successful open channel creation: %s (%s)',
            self.channel_id, self.address
        )

        return response

    def update(self, set_tags=None):
        """Update this OpenChannel object."""

        if self.tags and set_tags is None:
            raise ValueError(
                'set_tags may not be None when tags present on OpenChannel.'
            )

        if not self.address and not self.channel_id:
            raise ValueError('Must set address or channel ID to update.')

        if not self.open_platform:
            raise ValueError('Must set open_platform.')

        if not self.opt_in:
            raise ValueError('Must set opt_in.')

        if not self.address and self.opt_in is True:
            raise ValueError('Address must be set for opted in channels.')

        url = common.OPEN_CHANNEL_URL

        channel_data = {
            'type': 'open',
            'open': {'open_platform_name': self.open_platform},
            'opt_in': self.opt_in
        }
        if self.channel_id:
            channel_data['channel_id'] = self.channel_id
        if self.address:
            channel_data['address'] = self.address
        if self.tags:
            channel_data['tags'] = self.tags
            channel_data['set_tags'] = set_tags
        if self.identifiers:
            channel_data['open']['identifiers'] = self.identifiers

        body = json.dumps({'channel': channel_data})
        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            version=3
        )

        self.channel_id = response.json().get('channel_id')

        logger.info(
            'Successful open channel update: %s (%s)',
            self.channel_id, self.address
        )

        return response

    @classmethod
    def from_payload(cls, payload, airship):
        """Instantiate an OpenChannel from a payload."""
        obj = cls(airship)
        for key in payload:
            # Extract the open channel data
            if key == 'open':
                obj.open_platform = payload['open'].get('open_platform_name')
                obj.identifiers = payload['open'].get('identifiers', [])
                continue

            if key in ('created', 'last_registration'):
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], '%Y-%m-%dT%H:%M:%S'
                    )
                except:
                    payload[key] = 'UNKNOWN'
            setattr(obj, key, payload[key])

        return obj

    def lookup(self, channel_id):
        """Retrieves an open channel from the provided channel ID."""
        url = common.CHANNEL_URL + channel_id
        response = self.airship._request(
            method='GET',
            body=None,
            url=url,
            version=3
        )
        payload = response.json().get('channel')

        return self.from_payload(payload, self.airship)
