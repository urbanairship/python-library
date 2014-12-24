from urbanairship import common

class Tag(object):
	"""

    """

    params = {}
    url = common.TAGS_URL + tag_name
    response = airship._request('GET', None, url, version=3, params=params)
    payload = response.json()
    data_attribute = 'tags'
    id_key = 'tags'

    def __init__(self, airship, tag_name):
   
    def add(ios_channels=None, android_channels=None):
        issue this api request
    def remove(ios_channels=None, android_channels=None):
        issue this api request

tag = Tag(Airship, "high roller")
tag.add(android_channels=['12345-1231231'])

def tag_add(airship, tag_name, ios_channels, android_channels):
    add some stuff here :)


class TagList(DeviceList):    
    """
    Iterator for listing tags associated with this application.

    Will return the first 100 listings only.

    """

    start_url = common.TAGS_URL
    data_attribute = 'tags'
    tag_name = 'tags'
    params = {}
    url = start_url + ????_id
    response = airship._request('GET', None, url, version=3, params=params)
    payload = response.json()

    
class BatchTag():
    def __init__(self, airship):
        self.changelist = []

    def addIOSChannel(channel, tags):
        self.changelist.append({"ios_channel": channel, "tags": tags})

    def apply():
        issue api request

#  Leave out Create a Tag
 #   def createTag(self):
 #    """Optional call to create a tag not associated with any device.
    
    # """
 #        if not self.url:
 #            raise ValueError(
 #                "Cannot create a tag without url.")
 #        body = json.dumps(self.payload)
 #        response = self._airship._request('PUT', body,
 #            self.url, 'application/json', version=3)

 #        data = response.json()
 #        logger.info("Tag creation successful. tags_urls: %s",
 #            ', '.join(data.get('tags_urls', [])))

 #        return TagListResponse(?) 

   
    