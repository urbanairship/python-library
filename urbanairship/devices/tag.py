import json
import logging
#import urbanairship as ua


from urbanairship import common



logger = logging.getLogger('urbanairship')


class TagList(object):
    """Iterator for listing tags associated with this application.

    Will return the first 100 listings only.

    """

    def __init__(self, airship):
        self._airship = airship
        # self._airship.secret = 'secret'
        # self._airship.key = 'key'
#        self.tag_name = tag_name
        self.url = common.TAGS_URL
#        self.data_attribute = 'tags'

    def listTags(self, airship):

        response = airship._request('GET', None, self.url, version=3)
        
        # data = response.json()
        # logger.info("Listing successful.")
        # return data

class Tag(object):
    """Adding and Removing Devices from a Tag.

    """

    def __init__(self, airship, tag_name):
        self._airship = airship
        tag_name = tag_name
        self.url = common.TAGS_URL + '/' + tag_name
        self.payload = {}

    def add(self, ios_channels=None, android_channels=None, amazon_channels=None):
        # do a check to see if empty or not
        # if not empty, append
        # if empty, add

        if ios_channels is not None:
            if ios_channels not in self.payload:
                self.payload['ios_channels'] = {'add': [ios_channels]}
            else:
                if 'add' in self.payload['ios_channels']:
                    self.payload[ios_channels]['add'].extend(ios_channels)
                else:
                    self.payload['ios_channels']['add'] = [ios_channels]
        if android_channels not in self.payload:
            self.payload['android_channels'] = {'add': [self.android_channels]}
        else:
            if 'add' in self.payload['android_channels']:
                self.payload[android_channels]['add'].extend(android_channels)
            else:
                self.payload['android_channels']['add'] = [android_channels]
        if amazon_channels not in self.payload:
            self.payload['amazon_channels'] = {'add': [self.amazon_channels]}
        else:
            if 'add' in self.payload['amazon_channels']:
                self.payload[amazon_channels]['add'].extend(amazon_channels)
            else:
                self.payload['amazon_channels']['add'] = [amazon_channels]
        if not self.payload:
            raise ValueError('Cannot add a tag without a channel_id.')
        return self.payload

    def remove(self, ios_channels=None, android_channels=None, amazon_channels=None):
        # do a check to see if empty or not
        # if not empty, append
        # if empty, add

        if ios_channels not in self.payload:
            self.payload['ios_channels'] = {'remove': [self.ios_channels]}
        else:
            if 'remove' in self.payload['ios_channels']:
                self.payload[ios_channels]['remove'].extend(ios_channels)
            else:
                self.payload['ios_channels']['remove'] = [ios_channels]
        if android_channels not in self.payload:
            self.payload['android_channels'] = {'remove': [self.android_channels]}
        else:
            if 'remove' in self.payload['android_channels']:
                self.payload[android_channels]['remove'].extend(android_channels)
            else:
                self.payload['android_channels']['add'] = [android_channels]
        if amazon_channels not in self.payload:
            self.payload['amazon_channels'] = {'remove': [self.amazon_channels]}
        else:
            if 'add' in self.payload['amazon_channels']:
                self.payload[amazon_channels]['remove'].extend(amazon_channels)
            else:
                self.payload['amazon_channels']['remove'] = [amazon_channels]
        if not self.payload:
            raise ValueError('Cannot remove a tag without a channel_id.')
        return self.payload

    def apply(self):
        """Issues POST request for adding / removing device(s) to / from a tag.

        """

        body = json.dumps(self.payload)
        response = self._airship._request(Tag, 'POST', body,
                                          self.url, 'application/json', version=3)

        # data = response.json()
        # logger.info("Successful tag added to device channel.  %s",
        #             ', '.join(self.payload))


class DeleteTag(object):
    """Delete Tag from the System.

    - deletes tag from devices which are active / not uninstalled.
    - Devices which are uninstalled retain their tags.

    """
    def __init__(self, airship, tag_name):
        self._airship = airship
        self.tag_name = tag_name
        self.url = common.TAGS_URL + '/' + tag_name
        self._airship.secret = 'secret'
        self._airship.key = 'key'

        response = self.airship._request('DELETE', None, self.url, version=3)
        return response


class BatchTag(object):
    """Modify the tags for an assortment of devices.

    """

    def __init__(self, airship):
        self._airship = airship
        self.changelist = []
        self.url = common.TAGS_URL + '/batch'

    def addIOSChannel(self, channel, tags):
        self.changelist.append({"ios_channel": channel, "tags": tags})

    def addAndroidChannel(self, channel, tags):
        self.changelist.append({"android_channel": channel, "tags": tags})

    def addAmazonChannel(self, channel, tags):
        self.changelist.append({"amazon_channel": channel, "tags": tags})

    def apply(self):
        """Issue API Request

        - error message in the form of an object containing array of two member arrays
         - includes 1) the line that did not pass and 2) an error response

        """

        body = json.dumps(self.changelist)
        response = self._airship._request(self, 'POST', body, self.url, 'application/json',
                                          version=3)
        data = response.json()
        logger.info("Successful batch modification: %s",
                    ', '.join(self.changelist))
