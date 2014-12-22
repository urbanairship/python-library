from urbanairship import common

class CreateTag(object):
	"""
    Optional call to create a tag not associated with any device.
	
	"""

    


class ListTag(DeviceList)
    """
    Iterator for listing all of the tags for this application.

    [Need to implement a limit to the # of tags that can come back.  Check w/Mele (don't have access to those docs?)]
    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each "next" returns a :py:class:'????' object.

    """

     start_url = common.CHANNEL_URL
     data_attribute = 'tags'
     id_key = 'tag'

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