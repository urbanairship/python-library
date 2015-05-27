import json
import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')


class TagList(object):
    """List tags associated with this application.

    Will return the first 100 listings only.

    """

    def __init__(self, airship):
        self._airship = airship
        self.url = common.TAGS_URL

    def list_tags(self):

        response = self._airship._request('GET', None, self.url, version=3)

        logger.info("Tag listing successful.")
        return response.json()


class Tag(object):
    """Add and remove devices from a tag."""

    def __init__(self, airship, tag_name, group=None):
        self._airship = airship
        self.tag_name = tag_name
        self.url = common.CHANNEL_URL + 'tags/'

        if group is None:
            self.group = 'device'
        else:
            self.group = group

    def add(self, ios_channels=None, android_channels=None,
            amazon_channels=None):
        """Add channels to the add operation in the device payloads"""

        self.data = {}
        audience = {}

        if ios_channels is not None:
            audience['ios_channel'] = ios_channels
        if android_channels is not None:
            audience['android_channel'] = android_channels
        if amazon_channels is not None:
            audience['amazon_channel'] = amazon_channels

        self.data['audience'] = audience
        self.data['add'] = {self.group: self.tag_name}

        body = json.dumps(self.data)
        response = self._airship._request(
            'POST', body, self.url, 'application/json', version=3
        )
        return response

    def remove(self, ios_channels=None, android_channels=None,
               amazon_channels=None):
        """Add channels to the remove operation in the device payloads"""

        self.data = {}
        audience = {}

        if ios_channels is not None:
            audience['ios_channel'] = ios_channels
        if android_channels is not None:
            audience['android_channel'] = android_channels
        if amazon_channels is not None:
            audience['amazon_channel'] = amazon_channels

        self.data['audience'] = audience
        self.data['remove'] = {self.group: self.tag_name}

        body = json.dumps(self.data)
        response = self._airship._request(
            'POST', body, self.url, 'application/json', version=3
        )
        return response

    def set(self, ios_channels=None, android_channels=None,
               amazon_channels=None):
        """Add channels to the set operation in the device payloads"""

        self.data = {}
        audience = {}

        if ios_channels is not None:
            audience['ios_channel'] = ios_channels
        if android_channels is not None:
            audience['android_channel'] = android_channels
        if amazon_channels is not None:
            audience['amazon_channel'] = amazon_channels

        self.data['audience'] = audience
        self.data['set'] = {self.group: self.tag_name}

        body = json.dumps(self.data)
        response = self._airship._request(
            'POST', body, self.url, 'application/json', version=3
        )
        return response


class DeleteTag(object):
    """Delete Tag from the System.

    - Deletes tag from devices which are active / not uninstalled.
    - Devices which are uninstalled retain their tags.

    """

    def __init__(self, airship, tag_name):
        self._airship = airship
        self.tag_name = tag_name
        self.url = common.TAGS_URL + tag_name
        self._airship.secret = 'secret'
        self._airship.key = 'key'

    def send_delete(self):
        response = self._airship._request('DELETE', None, self.url, version=3)
        logger.info('Successful tag deletion: %s', self.tag_name)
        return response


class BatchTag(object):
    """Modify the tags for an assortment of devices.

    """

    def __init__(self, airship):
        self._airship = airship
        self.url = common.CHANNEL_URL + 'tags/'
        self.ios_payload = {}
        self.android_payload = {}
        self.amazon_payload = {}

    def add_ios_channel(self, channel, tags, group=None):
        self.ios_payload['audience'] = {}
        self.ios_payload['audience']['ios_channel'] = channel

        if group is not None:
            self.ios_payload['add'] = {group: tags}
        else:
            self.ios_payload['add'] = {'device': tags}

    def add_android_channel(self, channel, tags, group=None):
        self.android_payload['audience'] = {}
        self.android_payload['audience']['android_channel'] = channel

        if group is not None:
            self.android_payload['add'] = {group: tags}
        else:
            self.android_payload['add'] = {'device': tags}

    def add_amazon_channel(self, channel, tags, group=None):
        self.amazon_payload['audience'] = {}
        self.amazon_payload['audience']['amazon_channel'] = channel

        if group is not None:
            self.amazon_payload['add'] = {group: tags}
        else:
            self.amazon_payload['add'] = {'device': tags}

    def send_request(self):
        """Issue API Requests for all device types

        """
        response_list = []

        if self.ios_payload:
            body = json.dumps(self.ios_payload)
            response_list.append(
                self._airship._request('POST', body, self.url,
                                       'application/json', version=3)
            )
        if self.android_payload:
            body = json.dumps(self.android_payload)
            response_list.append(
                self._airship._request('POST', body, self.url,
                                       'application/json', version=3)
            )
        if self.amazon_payload:
            body = json.dumps(self.amazon_payload)
            response_list.append(
                self._airship._request('POST', body, self.url,
                                       'application/json', version=3)
            )

        if not response_list:
            logger.error('Unsuccessful batch modification: No channels added.')
        else:
            logger.info('Successful batch modification: %s', response_list)

        return response_list
