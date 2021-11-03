import json
import logging
from datetime import datetime
import re

logger = logging.getLogger("urbanairship")


class Attribute(object):
    """
    Creates an attribute object for use with the ModifyAttributes class to set or remove
    attributes from channel_ids and named_user_ids.

    :keyword action: required. The action that will be taken with the supplied
        attributes. Must be one of 'set' or 'remove'.
    :keyword key: Required. The attribute key to be set.
    :keyword value: Required, a string or int. If action is 'set', the value to set on
        the key.
    :keyword timestamp: Optional. a datetime.datetime object representing the time the
        attribute was modified. If not included, the time of modification call will be
        used.
    """

    def __init__(self, action, key, value=None, timestamp=None):
        self.action = action
        self.key = key
        self.value = value
        self.timestamp = timestamp

        if self.action == "set" and self.value is None:
            raise ValueError("A value must be included with 'set' actions")

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if value not in ["set", "remove"]:
            raise ValueError("Action must be one of 'set' or 'remove'")
        self._action = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = str(value)

    @property
    def timestamp(self):
        if not self._timestamp:
            return self._timestamp
        return self._timestamp.replace(microsecond=0).isoformat()

    @timestamp.setter
    def timestamp(self, value):
        if value is not None and type(value) is not datetime:
            raise ValueError("timestamp must be a datetime.datetime object")
        self._timestamp = value

    @property
    def payload(self):
        data = {}
        data["action"] = self.action
        data["key"] = self.key
        if self.value:
            data["value"] = self.value
        if self.timestamp:
            data["timestamp"] = self.timestamp

        return data


class ModifyAttributes(object):
    """
    Set or remove attributes on a channel. Aside from Airship's default attributes,
    you must define attributes in the Airship dashboard before you can set them on
    channels. A single channel_id or named_user must be included.

    :keyword airship: required. An Airship object.
    :keyword attributes: required. A list of one or more Attributes objects.
    :keyword channel: optional. An existing UUID formatted channel_id
    :keyword named_user: optional. An existing named_user_id
    """

    def __init__(self, airship, attributes, channel=None, named_user=None):
        self.airship = airship
        self.attributes = attributes
        self.channel = channel
        self.named_user = named_user

        if self.channel is None and self.named_user is None:
            raise ValueError("Either channel or named_user must be included")

        if self.channel is not None and self.named_user is not None:
            raise ValueError("Either channel or named_user must be included, not both")

    @property
    def attributes(self):
        return [attribute.payload for attribute in self._attributes]

    @attributes.setter
    def attributes(self, value):
        if type(value) is not list:
            raise ValueError("attributes must be a list of Attribute objects")
        self._attributes = value

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    @property
    def payload(self):
        data = {}
        audience = {}
        if self.channel:
            audience["channel"] = [self.channel]
        elif self.named_user:
            audience["named_user_id"] = [self.named_user]

        data["audience"] = audience
        data["attributes"] = self.attributes

        return data

    def send(self):
        """
        Makes the call to Airship APIs to modify the channel_id or named_user passed
        on init.

        :return AttributeResponse object
        """
        response = self.airship.request(
            method="POST",
            body=json.dumps(self.payload).encode("UTF-8"),
            url=self.airship.urls.get("attributes_url"),
            version=3,
        )

        return AttributeResponse(response=response)


class AttributeResponse(object):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return "Response Payload: {0}".format(self.response)

    @property
    def response(self):
        return self._response.json()

    @response.setter
    def response(self, value):
        self._response = value

    @property
    def ok(self):
        return self.response.get("ok")

    @property
    def warning(self):
        return self.response.get("warning")
