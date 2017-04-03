import json
import logging
import warnings
from urbanairship import common

logger = logging.getLogger('urbanairship')


class TagList(object):
    """List tags associated with this application.

    Will return the first 100 listings only.

    """

    def __init__(self, airship):
        warnings.warn(
            "The TagList object has been deprecated.",
            DeprecationWarning
        )
        self._airship = airship
        self.url = common.TAGS_URL

    def list_tags(self):
        response = self._airship._request('GET', None, self.url, version=3)

        logger.info("Tag listing successful.")
        return response.json()


class Tag(object):
    """Add and remove devices from a tag."""

    def __init__(self, airship, tag_name):
        warnings.warn(
            'The Tag object has been deprecated. Please use ChannelTags '
            'instead.',
            DeprecationWarning
        )
        self._airship = airship
        tag_name = tag_name
        self.url = common.TAGS_URL + tag_name

    def add(self, ios_channels=None, android_channels=None,
            amazon_channels=None):
        """Adds channels to 'data' dict and then sends POST request."""

        self.data = {}
        if ios_channels is not None:
            self.data['ios_channels'] = {'add': ios_channels}
        if android_channels is not None:
            self.data['android_channels'] = {'add': android_channels}
        if amazon_channels is not None:
            self.data['amazon_channels'] = {'add': amazon_channels}

        body = json.dumps(self.data)
        response = self._airship._request('POST', body, self.url,
                                          'application/json', version=3)
        return response

    def remove(self, ios_channels=None, android_channels=None,
               amazon_channels=None):
        """Add channels to remove to 'data' dict and sends POST request."""

        self.data = {}
        if ios_channels is not None:
            self.data['ios_channels'] = {'remove': ios_channels}
        if android_channels is not None:
            self.data['android_channels'] = {'remove': android_channels}
        if amazon_channels is not None:
            self.data['amazon_channels'] = {'remove': amazon_channels}

        body = json.dumps(self.data)
        response = self._airship._request('POST', body, self.url,
                                          'application/json', version=3)
        return response


class DeleteTag(object):
    """Delete Tag from the System.

    - Deletes tag from devices which are active / not uninstalled.
    - Devices which are uninstalled retain their tags.

    """

    def __init__(self, airship, tag_name):
        warnings.warn(
            "The DeleteTag object has been deprecated.",
            DeprecationWarning
        )
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
        warnings.warn(
            'The BatchTag object has been deprecated. Please use ChannelTags ' +
            'instead.',
            DeprecationWarning
        )
        self._airship = airship
        self.changelist = []
        self.url = common.TAGS_URL + '/batch/'

    def add_ios_channel(self, channel, tags):
        self.changelist.append({'ios_channel': channel, 'tags': tags})

    def add_android_channel(self, channel, tags):
        self.changelist.append({'android_channel': channel, 'tags': tags})

    def add_amazon_channel(self, channel, tags):
        self.changelist.append({'amazon_channel': channel, 'tags': tags})


    def send_request(self):
        """Issue API Request

        - error message in the form of an obj containing array of two member
          arrays
        - includes 1) the line that did not pass and 2) an error response

        """

        body = json.dumps(self.changelist)
        response = self._airship._request('POST', body, self.url,
                                          'application/json', version=3)

        logger.info('Successful batch modification: %s', self.changelist)
        return response


class ChannelTags(object):
    """Modify the tags for a channel"""

    def __init__(self, airship):
        self.url = common.CHANNEL_URL + 'tags/'
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
