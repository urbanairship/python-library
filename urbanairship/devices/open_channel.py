import datetime
import json
import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')


class OpenChannel(object):
    _airship = None

    channel_id = None
    address = None
    open_platform = None
    identifiers = None
    opt_in = None
    installed = None
    created = None
    last_registration = None
    tags = None

    def create(self, airship, set_tags=None, hydrate=True):
        """Create this OpenChannel object with the API."""

        if self.tags and set_tags is None:
            raise ValueError(
                'set_tags may not be None when tags present on OpenChannel.'
            )

        if not self.address:
            raise ValueError('Must set address before creation.')

        if not self.open_platform:
            raise ValueError('Must set open_platforn before creation.')

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
        response = airship.request(
            method='POST',
            body=body,
            url=url,
            version=3
        )

        self.channel_id = response.json().get('channel_id')

        logger.info(
            'Successful open channel creation: {} ({})'.format(
                self.channel_id, self.address
            )
        )

        if hydrate:
            payload = self._get_payload_for_id(airship, self.channel_id)
            self.from_payload(payload)

        return response

    def update(self, airship, set_tags=None):
        """Update this OpenChannel object."""

        if self.tags and set_tags is None:
            raise ValueError(
                'set_tags may not be None when tags present on OpenChannel.'
            )

        if not self.address or not self.channel_id:
            raise ValueError('Must set address or channel ID to update.')

        if not self.open_platform:
            raise ValueError('Must set open_platforn.')

        url = common.OPEN_CHANNEL_URL

        channel_data = {
            'type': 'open',
            'open': {'open_platform_name': self.open_platform}
        }

        if self.channel_id:
            channel_data['channel_id'] = self.channel_id
        if self.address:
            channel_data['address'] = self.address
        if self.opt_in is not None:
            channel_data['opt_in'] = self.opt_in
        if self.tags:
            channel_data['tags'] = self.tags
            channel_data['set_tags'] = set_tags
        if self.identifiers:
            channel_data['open']['identifiers'] = self.identifiers

        body = json.dumps({'channel': channel_data})
        response = airship.request(
            method='POST',
            body=body,
            url=url,
            version=3
        )

        self.channel_id = response.json().get('channel_id')

        logger.info(
            'Successful open channel update: {} ({})'.format(
                self.channel_id, self.address
            )
        )

        return response

    def from_payload(self, payload):
        """Set attributes of the OpenChannel from a payload."""
        for key in payload:
            # Extract the open channel data
            if key == 'open':
                self.open_platform = payload['open'].get('open_platform_name')
                self.identifiers = payload['open'].get('identifiers', [])
                continue

            if key in ('created', 'last_registration'):
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], '%Y-%m-%dT%H:%M:%S'
                    )
                except:
                    payload[key] = "UNKNOWN"
            setattr(self, key, payload[key])

        return self

    @staticmethod
    def _get_payload_for_id(airship, channel_id):
        url = common.CHANNEL_URL + channel_id
        response = airship._request(
            method='GET',
            body=None,
            url=url,
            version=3
        )
        return response.json()['channel']

    @classmethod
    def from_id(cls, airship, channel_id):
        """Retrieves an open channel from the provided channel ID."""

        payload = cls._get_payload_for_id(airship, channel_id)

        obj = cls()
        return obj.from_payload(payload)
