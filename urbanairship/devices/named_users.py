import json
import logging

from urbanairship.devices import ChannelTags
from urbanairship import common
from urbanairship.push.payload import device_types

logger = logging.getLogger("urbanairship")


class NamedUser(object):
    """Perform various operations on a named user object"""

    def __init__(self, airship, named_user_id=None):

        self._airship = airship
        self.named_user_id = named_user_id
        self.channel_id = None
        self.email_address = None
        self.device_type = None

    @property
    def _channel_associate_payload(self):
        """
        creates the paylaod for channel_id associate and disassociate calls
        """
        payload = {"named_user_id": self.named_user_id, "channel_id": self.channel_id}

        if self.device_type:
            payload["device_type"] = self.device_type

        return payload

    @property
    def _email_associate_payload(self):
        """
        creates the payload for email_address associate and disassociate calls
        """
        return {
            "named_user_id": self.named_user_id,
            "email_address": self.email_address,
        }

    def _dis_associate(self, url, body):
        response = self._airship.request(
            method="POST",
            body=json.dumps(body),
            url=url,
            content_type="application/json",
            version=3,
        )

        return response

    def associate(self, channel_id, device_type=None):
        """Associate a channel_id  with a named user ID.
        Either channel_id and device_type OR email_address must be included.

        :param channel_id: Required. The ID of the channel you would like to associate
            with the named user
        :param device_type: The device type of the channel, do not include for web
            notify channel_ids

        :return:
        """
        if not self.named_user_id:
            raise ValueError("named_user_id is required for association")

        self.channel_id = channel_id

        if device_type:
            self.device_type = device_type

        return self._dis_associate(
            url=self._airship.urls.get("named_user_associate_url"),
            body=self._channel_associate_payload,
        )

    def email_associate(self, email_address):
        """Associate an email_address with a named user id. This call is for a literal
            email address.

        :param email_address: Required. The email address to associate.

        :return:
        """
        if not self.named_user_id:
            raise ValueError("named_user_id is required for association")

        self.email_address = email_address

        return self._dis_associate(
            url=self._airship.urls.get("named_user_associate_url"),
            body=self._email_associate_payload,
        )

    def disassociate(self, channel_id, device_type=None):
        """Disassociate a channel with a named user ID

        :param channel_id: The ID of the channel you would like to disassociate
        :param device_type: The device type of the channel. Do not include for web
            notify channels.

        :return:
        """
        if not self.named_user_id:
            raise ValueError("named_user_id is required for association")

        self.channel_id = channel_id

        if device_type:
            self.device_type = device_type

        return self._dis_associate(
            url=self._airship.urls.get("named_user_disassociate_url"),
            body=self._channel_associate_payload,
        )

    def email_disassociate(self, email_address):
        """Disassociate an email_address with a named user ID

        :param channel_id: The email_address you would like to disassociate

        :return:
        """
        if not self.named_user_id:
            raise ValueError("named_user_id is required for association")

        self.email_address = email_address

        return self._dis_associate(
            url=self._airship.urls.get("named_user_disassociate_url"),
            body=self._email_associate_payload,
        )

    def lookup(self):
        """Lookup a single named user

        :return: The named user payload for the named user ID
        """
        response = self._airship._request(
            "GET",
            None,
            self._airship.urls.get("named_user_url"),
            "application/json",
            version=3,
            params={"id": self.named_user_id},
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
            payload = {"audience": {"named_user_id": self.named_user_id}}
        else:
            raise ValueError("A named user ID is required for modifying tags")

        if add:
            if set:
                raise ValueError(
                    "A tag request can only contain an add or "
                    "remove field, both, or a single set field"
                )
            payload["add"] = {group: add}

        if remove:
            if set:
                raise ValueError(
                    "A tag request can only contain an add or "
                    "remove field, both, or a single set field"
                )
            payload["remove"] = {group: remove}

        if set:
            payload["set"] = {group: set}
        if not add and not remove and not set:
            raise ValueError("An add, remove, or set field was not set")

        body = json.dumps(payload).encode("utf-8")
        response = self._airship._request(
            "POST",
            body,
            self._airship.urls.get("named_user_tag_url"),
            "application/json",
            version=3,
        )

        return response.json()

    def update(self, associate=None, disassociate=None, tags=None, attributes=None):
        """
        Create or update a named user by associating/disassociating channels
            and adding/removing tags and attributes in a single request.
        If a channel has an assigned named user and you make an additional call to
            associate that same channel with a new named user, the original named user
            association will be removed and the new named user and associated data will
            take its place. Additionally, all tags associated to the original named
            user cannot be used to address this channel unless they are also associated
            with the new named user.

        Please see https://docs.airship.com/api/ua/#operation-api-named_users-named_user_id-post

        :param assocaite: Optional. List of objects to associate with the named user
        :param disassociate: Optional. List of objects to disassociate from the named
            user
        :param tags: Optional. Dictionary of set, add, remove objects to apply to
            named user
        :param attributes: Optional. List of attributes to apply to named user.

        :return:
        """
        if not any([associate, disassociate, tags, attributes]):
            raise ValueError(
                "At least one of associate, disassociate, tags, or attributes must be included"
            )

        body = {}

        if associate:
            body["associate"] = associate
        if disassociate:
            body["disassociate"] = disassociate
        if tags:
            body["tags"] = tags
        if attributes:
            body["attributes"] = attributes

        response = self._airship.request(
            method="POST",
            body=json.dumps(body),
            url=self._airship.urls.get("named_user_url") + self.named_user_id,
            content_type="application/json",
            version=3,
        )

        return response

    def attributes(self, attributes):
        """
        Set or remove attributes on a named user.
        A single request body may contain a set or remove field, or both, or a single
        set field. If both set and remove fields are present and the intersection of
        the attributes in these fields is not empty, then a 400 will be returned.
        If an attribute request is partially valid, i.e. at least one attribute exists,
        Airship returns a 200 with a warning in containing a list of attributes that
        failed to update.
        Please see https://docs.airship.com/api/ua/#operation-api-named_users-named_user_id-attributes-post
            for more about using Airship attributes.

        :params attributes: Required. A list of attribute objects to set or remove on
            the named user.
        """
        if type(attributes) is not list:
            raise ValueError("attributes must be a list of attribute objects")

        response = self._airship.request(
            method="POST",
            body=json.dumps({"attributes": attributes}),
            url=self._airship.urls.get("named_user_url")
            + self.named_user_id
            + "attributes",
            content_type="application/json",
            version=3,
        )

        return response

    @classmethod
    def uninstall(cls, airship, named_users):
        """
        Disassociate and delete all channels associated with the named_user_id(s) and
        also delete the named_user_id(s). This call removes all channels associated
        with a named user from Airship systems in compliance with data privacy laws.
        Uninstalling channels also removes accompanying analytic data (including
        Performance Analytics) from the system.
        Channel uninstallation, like channel creation, is an asynchronous operation,
        and may take some time to complete.

        :param airship: Required. An urbanairship.Airship instance.
        :param named_users: Required a list of named_user_ids to completely uninstall

        :return:
        """
        if type(named_users) is not list:
            raise ValueError("named_users must be a list")

        response = airship.request(
            method="POST",
            body=json.dumps({"named_user_id": named_users}),
            url=airship.urls.get("named_user_uninstall_url"),
            content_type="application/json",
            version=3,
        )

        return response

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

    next_url = None
    data_attribute = "named_users"

    def __init__(self, airship):
        self.next_url = airship.urls.get("named_user_url")
        super(NamedUserList, self).__init__(airship, None)


class NamedUserTags(ChannelTags):
    """Modify the tags for named users"""

    def __init__(self, airship):
        super(NamedUserTags, self).__init__(airship)
        self.url = airship.urls.get("named_user_tag_url")

    def set_audience(self, user_ids):
        self.audience["named_user_id"] = user_ids
