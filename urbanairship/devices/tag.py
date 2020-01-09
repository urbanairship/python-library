import json
import logging

logger = logging.getLogger('urbanairship')


class ChannelTags(object):
    """Modify the tags for a channel"""

    def __init__(self, airship):
        self.url = airship.urls.get('channel_url') + 'tags/'
        self._airship = airship
        self.audience = {}
        self.add_group = {}
        self.remove_group = {}
        self.set_group = {}

    def set_audience(self, ios=None, android=None, amazon=None, web=None):
        if ios is not None:
            self.audience['ios_channel'] = ios
        if android is not None:
            self.audience['android_channel'] = android
        if amazon is not None:
            self.audience['amazon_channel'] = amazon
        if web is not None:
            self.audience['channel'] = web

    def add(self, group_name, tags):
        self.add_group[group_name] = tags

    def remove(self, group_name, tags):
        self.remove_group[group_name] = tags

    def set(self, group_name, tags):
        self.set_group[group_name] = tags

    def send(self):
        payload = {}

        if not self.audience:
            raise ValueError('A audience is required for modifying tags')
        payload['audience'] = self.audience

        if self.add_group:
            if self.set_group:
                raise ValueError('A tag request cannot contain both an "add"'
                                 ' and a "set" field.')
            payload['add'] = self.add_group

        if self.remove_group:
            if self.set_group:
                raise ValueError('A tag request cannot contain both a "remove"'
                                 ' and a "set" field.')
            payload['remove'] = self.remove_group

        if self.set_group:
            payload['set'] = self.set_group

        if not self.add_group and not self.remove_group and not self.set_group:
            raise ValueError('An add, remove, or set field was not set')

        body = json.dumps(payload)
        response = self._airship._request(
            'POST', body, self.url,
            'application/json', version=3
        )
        return response.json()


class OpenChannelTags(object):
    """Modify the tags for an open channel"""

    def __init__(self, airship):
        self.url = airship.urls.get('open_channel_url') + 'tags/'
        self._airship = airship
        self.audience = {}
        self.add_group = {}
        self.remove_group = {}
        self.set_group = {}

    def set_audience(self, address, open_platform):
        self.audience = {
            'address': address,
            'open_platform_name': open_platform
        }

    def add(self, group_name, tags):
        self.add_group[group_name] = tags

    def remove(self, group_name, tags):
        self.remove_group[group_name] = tags

    def set(self, group_name, tags):
        self.set_group[group_name] = tags

    def send(self):
        payload = {}

        if not self.audience:
            raise ValueError('An audience is required to modify tags')
        payload['audience'] = self.audience

        if not self.add_group and not self.remove_group and not self.set_group:
            raise ValueError('An add, remove, or set field was not set')

        if self.set_group:
            if self.add_group or self.remove_group:
                raise ValueError('A "set" tag request cannot contain '
                                 '"add" or "remove" fields')
            payload['set'] = self.set_group

        if self.add_group:
            payload['add'] = self.add_group

        if self.remove_group:
            payload['remove'] = self.remove_group

        body = json.dumps(payload)
        response = self._airship._request(
            'POST', body, self.url,
            'application/json', version=3
        )
        return response.json()
