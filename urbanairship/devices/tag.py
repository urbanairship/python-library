import json
import logging

from urbanairship import common
from urbanairship import core


logger = logging.getLogger('urbanairship')


class TagList(object):
    """Iterator for listing tags associated with this application.

    Will return the first 100 listings only.
    Returns: 

    """

    url = common.TAGS_URL
    data_attribute = 'tags'
    tag_name = 'tags'
#    params = {}

    response = self.airship._request('GET', None, url, version=3)  #error here regarding 'airship'
#    return response.json()
#    payload = response.json()

    
# #  **********************Leave out Tag Creation*******
#  #   def createTag(self):
#  #    """Optional call to create a tag not associated with any device.
    
#     # """
#  #        if not self.url:
#  #            raise ValueError(
#  #                "Cannot create a tag without url.")
#  #        body = json.dumps(self.payload)
#  #        response = self._airship._request('PUT', body,
#  #            self.url, 'application/json', version=3)

#  #        data = response.json()
#  #        logger.info("Tag creation successful. tags_urls: %s",
#  #            ', '.join(data.get('tags_urls', [])))

#  #        return TagListResponse(?) 

   
class Tag(object):
    """Adding and Removing Devices from a Tag.
       Adding and Removing Tags from a Device.

    """

    def __init__(self, airship, tag_name):
        self._airship = airship
        self.tag_name = tag_name
        self.ios_channel = None
        self.android_channel = None
        self.amazon_channel = None
        self.payload = None
   

    def add(self, ios_channels=None, android_channels=None, amazon_channels=None):
        """Add device to a tag.

        """


        payload = {}
        if ios_channels is not None:
            payload['ios_channels'] = {'add': ios_channels}
        if android_channels is not None:
            payload['android_channels'] = {'add': android_channels}
        if amazon_channels is not None:
            payload['amazon_channels'] = {'add': amazon_channels}
        if not payload:
            raise ValueError('Cannot add a tag without a channel_id.')
        

        body = json.dumps(self.payload)
        response = self._airship._request(Airship, 'POST', body,
            common.TAGS_URL + '/' + self.tag_name, 'application/json', version=3)

        #data = response.json()
        #logger.info("Successful tag added to device channel. tag_name: %s",
        #     ', '.join(tag_name))
   

    def remove(self, ios_channels=None, android_channels=None):
        """Remove device from a tag.

        """


        payload = {}
        if ios_channels is not None:
            payload['ios_channels'] = {'remove': ios_channels} #need to write 'ios_channels' as a list?
        if android_channels is not None:
            payload['android_channels'] = {'remove': android_channels}
        if amazon_channels is not None:
            payload['amazon_channels'] = {'remove': amazon_channels}
        else:
            raise ValueError('Cannot remove a tag without a channel_id.')
        

        body = json.dumps(self.payload)
        response = self._airship._request('POST', body,
            common.TAGS_URL + '/' + self.tag_name, 'application/json', version=3)

        #data = response.json()
        #logger.info("Successful, tag removed.")


    # def tag_add(airship, tag_name, ios_channels, android_channels, amazon_channels):
    #     """

    #     """

class DeleteTag(Airship, tag_name):
    """Delete Tag from the System.

    - deletes tag from devices which are active / not uninstalled.
    - Devices which are uninstalled retain their tags.

    """
    url = common.TAGS_URL + '/' + tag_name
    data_attribute = 'tags'
    tag_name = 'tags'
#    params = {}

    response = self.airship._request('DELETE', None, url, version=3)  #error here regarding 'airship'
#    return response.json()
#    payload = response.json()

# class BatchTag():
#     def __init__(self, airship):
#         self.changelist = []


#     def addIOSChannel(channel, tags):
#         self.changelist.append({"ios_channel": channel, "tags": tags})


#     def addAndroidChannel(channel, tags):
#         self.changelist.append({"android_channel": channel, "tags": tags})


#     def addAmazonChannel(channel, tags):
#         self.changelist.append({"amazon_channel": channel, "tags": tags})


#     def apply():
#         issue api request

