import json
import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')


class NamedUser(object):
    """Perform various operations on a named user object"""

    def __init__(self, airship, named_user_id=None):

        self._airship = airship
        self.named_user_id = named_user_id

    def associate(self, channel_id, device_type):
        """Associate a channel with a named user ID

        :param channel_id: The ID of the channel you would like to associate
            with the named user
        :param device_type: The device type of the channel
        :return:
        """
        if not self.named_user_id:
            raise ValueError('named_user_id is required for association')

        body = json.dumps(
            {
                'channel_id': channel_id,
                'device_type': device_type,
                'named_user_id': self.named_user_id
            }
        ).encode('utf-8')
        response = self._airship._request(
            'POST',
            body,
            common.NAMED_USER_ASSOCIATE_URL,
            'application/json',
            version=3
        )
        return response

    def disassociate(self, channel_id, device_type):
        """Disassociate a channel with a named user ID

        :param channel_id: The ID of the channel you would like to disassociate
        :param device_type: The device type of the channel
        :return:
        """

        payload = {'channel_id': channel_id, 'device_type': device_type}

        if self.named_user_id:
            payload['named_user_id'] = self.named_user_id

        body = json.dumps(payload).encode('utf-8')
        response = self._airship._request(
            'POST',
            body,
            common.NAMED_USER_DISASSOCIATE_URL,
            'application/json',
            version=3
        )

        return response

    def lookup(self):
        """Lookup a single named user

        :return: The named user payload for the named user ID
        """
        response = self._airship._request(
            'GET',
            None,
            common.NAMED_USER_URL,
            'application/json',
            version=3,
            params={'id': self.named_user_id}
        )
        return response.json()

    def tag(self, group, add=None, remove=None, set=None):
        """Add, remove, or set tags on a named user
        :param add: A list of tags to add
        :param remove: A list of tags to remove
        :param set: A list of tags to set
        :param group: The Tag group for the add, remove, and set operations
        """
        if self.named_user_id:
            payload = {'audience': {'named_user_id': self.named_user_id}}
        else:
            raise ValueError('A named user ID is required for modifying tags')

        if add:
            if set:
                raise ValueError('A tag request can only contain an add or '
                                 'remove field, both, or a single set field')
            payload['add'] = {group: add}

        if remove:
            if set:
                raise ValueError('A tag request can only contain an add or '
                                 'remove field, both, or a single set field')
            payload['remove'] = {group: remove}

        if set:
            payload['set'] = {group: set}
        if not add and not remove and not set:
            raise ValueError('An add, remove, or set field was not set')

        body = json.dumps(payload).encode('utf-8')
        response = self._airship._request(
            'POST',
            body,
            common.NAMED_USER_TAG_URL,
            'application/json',
            version=3
        )

        return response.json()

    @classmethod
    def from_payload(cls, payload):
        """
        Create NamedUser object based on results from a NamedUserList iterator.
        :param payload: Payload used to create the NamedUser object

        """
        for key in payload:
            setattr(cls, key, payload[key])

        return cls


class NamedUserList(common.IteratorParent):
    """Retrieves a list of NamedUsers"""
    next_url = common.NAMED_USER_URL
    data_attribute = 'named_users'

    def __init__(self, airship):
        super(NamedUserList, self).__init__(airship, None)
