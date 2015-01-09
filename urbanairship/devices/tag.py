import json
import logging
# import urbanairship as ua


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
        self.url = common.TAGS_URL + '/'
#        self.data_attribute = 'tags'

    def listTags(self):

        response = self._airship._request('GET', None, self.url, version=3)

        logger.info("Listing successful.")
        #print response.json()
        return response.json()


class Tag(object):
    """Adding and Removing Devices from a Tag.

    """

    def __init__(self, airship, tag_name):
        self._airship = airship
        tag_name = tag_name
        self.url = common.TAGS_URL + '/' + tag_name
        self.data = {}

    def add(self, ios_channels=None, android_channels=None,
            amazon_channels=None):
        """-add channels to data
           -POST request

        """
        if ios_channels is not None:
            self.data['ios_channels'] = {'add': ios_channels}
        if android_channels is not None:
            self.data['android_channels'] = {'add': android_channels}
        if amazon_channels is not None:
            self.data['amazon_channels'] = {'add': amazon_channels}

        body = json.dumps(self.data)
        response = self._airship._request('POST', body,
                                      self.url, 'application/json', version=3)

    def remove(self, ios_channels=None, android_channels=None,
               amazon_channels=None):
        """Removing from obj

        - pass in a list of channels
        - add that as a dict to the data obj

        """

        if ios_channels is not None:
            self.data['ios_channels'] = {'remove': ios_channels}
        if android_channels is not None:
            self.data['android_channels'] = {'remove': android_channels}
        if amazon_channels is not None:
            self.data['amazon_channels'] = {'remove': amazon_channels}
        return self.data

        body = json.dumps(self.data)
        response = self._airship._request('POST', body,
                                          self.url, 'application/json', version=3)


class DeleteTag(object):
    """Delete Tag from the System.

    - deletes tag from devices which are active / not uninstalled.
    - Devices which are uninstalled retain their tags.

    """
    def __init__(self, airship, tag_name):
        self._airship = airship
        self.tag_name = tag_name
        self.url = common.TAGS_URL + '/' + tag_name
        # self._airship.secret = 'secret'
        # self._airship.key = 'key'

    def send_delete(self):

        response = self._airship._request('DELETE', None, self.url, version=3)
        logger.info("Successful deletion")
        print response
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

    def send_request(self):
        """Issue API Request

        - error message in the form of an obj containing array of two member arrays
         - includes 1) the line that did not pass and 2) an error response

        """

        body = json.dumps(self.changelist)
        response = self._airship._request('POST', body, self.url,
                                          'application/json', version=3)
        data = response.json()
        logger.info("Successful batch modification: %s", self.changelist)
