import json
import logging

from urbanairship import common
from urbanairship import core


logger = logging.getLogger('urbanairship')

class TagList():
    """Iterator for listing tags associated with this application.

    Will return the first 100 listings only.
    Returns: 

    """

    def __init__(self, airship, tag_name):
        self._airship = airship
        self._airship.secret = secret
        self._airship.key = key
        self.tag_name = tag_name
        self.url = common.TAGS_URL
        self.data_attribute = 'tags' 

        response = airship._request('GET', None, url, version=3)
        return response.json()


class Tag(object):
    """Adding and Removing Devices from a Tag.

    """

    def __init__(self, airship, tag_name):
        self._airship = airship
        self.url = common.TAGS_URL + '/' + tag_name
        self.payload = None
   

    def add(self, ios_channels=None, android_channels=None, amazon_channels=None):
        # do a check to see if empty or not
        #if not empty, append
        #if empty, add

        if isinstance(ios_channels):
            ios_channels = [ios_channels]
        if ios_channels not in self.payload:
            self.payload['ios_channels'] = {'add': [self.ios_channels]}
        else:
            if 'add' in self.payload['ios_channels']:
                self.payload[ios_channels]['add'].extend(ios_channels)
            else:
                self.payload['ios_channels']['add'] = [ios_channels]
        if isinstance(android_channels):
            android_channels = [android_channels]
        if android_channels not in self.payload:
            self.payload['android_channels'] = {'add': [self.android_channels]}
        else:
            if 'add' in self.payload['android_channels']:
                self.payload[android_channels]['add'].extend(android_channels)
            else:
                self.payload['android_channels']['add'] = [android_channels]
        if isinstance(amazon_channels):
            amazon_channels = [amazon_channels]
        if amazon_channels not in self.payload:
            self.payload['amazon_channels'] = {'add': [self.amazon_channels]}
        else:
            if 'add' in self.payload['amazon_channels']:
                self.payload[amazon_channels]['add'].extend(amazon_channels)
            else:
                self.payload['amazon_channels']['add'] = [amazon_channels]
        if not data:
            raise ValueError('Cannot add a tag without a channel_id.')
        return payload


    def remove(self, ios_channels=None, android_channels=None, amazon_channels=None):
        # do a check to see if empty or not
        #if not empty, append
        #if empty, add

        if isinstance(ios_channels):
            ios_channels = [ios_channels]
        if ios_channels not in self.payload:
            self.payload['ios_channels'] = {'remove': [self.ios_channels]}
        else:
            if 'remove' in self.payload['ios_channels']:
                self.payload[ios_channels]['remove'].extend(ios_channels)
            else:
                self.payload['ios_channels']['remove'] = [ios_channels]
        if isinstance(android_channels):
            android_channels = [android_channels]
        if android_channels not in self.payload:
            self.payload['android_channels'] = {'remove': [self.android_channels]}
        else:
            if 'remove' in self.payload['android_channels']:
                self.payload[android_channels]['remove'].extend(android_channels)
            else:
                self.payload['android_channels']['add'] = [android_channels]
        if isinstance(amazon_channels):
            amazon_channels = [amazon_channels]
        if amazon_channels not in self.payload:
            self.payload['amazon_channels'] = {'remove': [self.amazon_channels]}
        else:
            if 'add' in self.payload['amazon_channels']:
                self.payload[amazon_channels]['remove'].extend(amazon_channels)
            else:
                self.payload['amazon_channels']['remove'] = [amazon_channels]
        if not data:
            raise ValueError('Cannot remove a tag without a channel_id.')
        return payload


    def apply(self):
        """Issues POST request for adding / removing device(s) to / from a tag.

        """

        body = json.dumps(self.data)
        response = self._airship._request(Airship, 'POST', body,
            self.url, 'application/json', version=3)

        data = response.json()
        logger.info("Successful tag added to device channel. tag_name: %s",
             ', '.join(tag_name))


# """ 
# Test:  tag = Tag(Airship, "high roller")
#        tag.add_remove(android_channels={"add": ['9c36e8c7-5a73-47c0-9716-99fd3d4197d5']})
# """

class DeleteTag(object):
    """Delete Tag from the System.

    - deletes tag from devices which are active / not uninstalled.
    - Devices which are uninstalled retain their tags.

    """
    def __init__(self, airship, tag_name):
        self._airship = airship
        self.tag_name = tag_name
        self.url = common.TAGS_URL + '/' + tag_name
        self._airship.secret = secret
        self._airship.key = key


        response = self.airship._request('DELETE', None, url, version=3)
        return response


# class BatchTag():
#     def __init__(self, airship):
#         self.changelist = []
#         self.url = common.TAGS_URL + '/batch'


#     def addIOSChannel(channel, tags):
#         self.changelist.append({"ios_channel": channel, "tags": tags})


#     def addAndroidChannel(channel, tags):
#         self.changelist.append({"android_channel": channel, "tags": tags})


#     def addAmazonChannel(channel, tags):
#         self.changelist.append({"amazon_channel": channel, "tags": tags})


#    def apply():
#        """Issue API Request

#        """

#        body = json.dumps(self.payload)
#        response = self._airship._request('POST', body, url, 'application/json', 
    #                                       version=3)

#        data = response.json()
#        logger.info("Successful batch modification: %s",
#             ', '.join(data))       