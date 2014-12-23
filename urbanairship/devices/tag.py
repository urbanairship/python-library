from urbanairship import common

class Tag(object):
	"""
    Optional call to create a tag not associated with any device.
	
	"""

    def createTag(self):
        if not self.url:
            raise ValueError(
                "Cannot create a tag without url.")
        body = json.dumps(self.payload)
        response = self._airship._request('PUT', body,
            self.url, 'application/json', version=3)

        data = response.json()
        logger.info("Tag creation successful. tags_urls: %s",
            ', '.join(data.get('tags_urls', [])))

        return TagListResponse()   #arg?

class TagListResponse(object):           ## I don't know if this class is necessary or in the right place!
    """Respone 

    Right now this is a fairly simple wrapper around the json payload response,
    but making it an object gives us some flexibility to add functionality
    later.

    """
    ok = None
    tag_ids = None
    tags_url = None
    payload = None

    def __init__(self, response):
        data = response.json()
        self.tag_ids = data.get('tags')
        self.tags_url = data.get('tags_urls', [None])[0]
        self.ok = data.get('ok')
        self.payload = data

    def __str__(self):
        return "Response Payload: {0}".format(self.payload)


    


class ListTag(DeviceList)     
    """
    Iterator for listing all of the tags for this application.

    Will return the first 100 listings.
    :returns: 

    """

     start_url = common.TAGS_URL
     data_attribute = 'tag'
     id_key = 'tags'

     def next(self):
         try:
             return ChannelInfo.from_payload(self._token_iter.next(), self.id_key)
         except StopIteration:
             self._fetch_next_page()
             return ChannelInfo.from_payload(self._token_iter.next(), self.id_key)


#class AddTag(object)
#    """
#    
#    """


#class RemoveTag(object)
#class BatchTag(object)