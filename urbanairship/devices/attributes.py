import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

from requests import Response

from urbanairship import Airship

from .static_lists import GzipCompressReadStream

logger = logging.getLogger("urbanairship")


class Attribute(object):
    """
    Creates an attribute object for use with the ModifyAttributes class to set or remove
    attributes from channel_ids and named_user_ids.

    :keyword action: [required] The action that will be taken with the supplied
        attributes. Must be one of 'set' or 'remove'.
    :keyword key: [required] The attribute key to be set.
    :keyword value: [required] a string or int. If action is 'set', the value to set on
        the key.
    :keyword timestamp: [optional] a datetime.datetime object representing the time the
        attribute was modified. If not included, the time of modification call will be
        used.
    """

    def __init__(
        self,
        action: str,
        key: str,
        value: Optional[Union[str, int]] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        self.action = action
        self.key = key
        self.value = value
        self.timestamp = timestamp

        if self.action == "set" and self.value is None:
            raise ValueError("A value must be included with 'set' actions")

    @property
    def action(self) -> str:
        return self._action

    @action.setter
    def action(self, value: str) -> None:
        if value not in ["set", "remove"]:
            raise ValueError("Action must be one of 'set' or 'remove'")
        self._action = value

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        self._key = str(value)

    @property
    def timestamp(self) -> Optional[datetime]:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime) -> None:
        if value is not None and type(value) is not datetime:
            raise ValueError("timestamp must be a datetime.datetime object")
        self._timestamp = value

    @property
    def payload(self) -> Dict:
        data: Dict = {}
        data["action"] = self.action
        data["key"] = self.key
        if self.value:
            data["value"] = self.value
        if isinstance(self.timestamp, datetime):
            data["timestamp"] = self.timestamp.replace(microsecond=0).isoformat()

        return data


class AttributeResponse(object):
    def __init__(self, response: Response):
        self.response = response

    def __str__(self) -> str:
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

    def __init__(
        self,
        airship: Airship,
        attributes: List[Attribute],
        channel: Optional[str] = None,
        named_user: Optional[str] = None,
    ) -> None:
        self.airship = airship
        self.attributes = attributes
        self.channel = channel
        self.named_user = named_user

        if self.channel is None and self.named_user is None:
            raise ValueError("Either channel or named_user must be included")

        if self.channel is not None and self.named_user is not None:
            raise ValueError("Either channel or named_user must be included, not both")

    @property
    def attributes(self) -> List[Attribute]:
        return self._attributes

    @attributes.setter
    def attributes(self, value: List[Attribute]):
        if type(value) is not list:
            raise ValueError("attributes must be a list of Attribute objects")
        self._attributes = value

    @property
    def channel(self) -> Optional[str]:
        return self._channel

    @channel.setter
    def channel(self, value: Optional[str]) -> None:
        self._channel = value

    @property
    def payload(self) -> Dict[str, Any]:
        data: Dict = {}
        audience: Dict = {}
        if self.channel:
            audience["channel"] = [self.channel]
        elif self.named_user:
            audience["named_user_id"] = [self.named_user]

        data["audience"] = audience
        data["attributes"] = [attribute.payload for attribute in self.attributes]

        return data

    def send(self) -> AttributeResponse:
        """
        Makes the call to Airship APIs to modify the channel_id or named_user passed
        on init.

        :return: AttributeResponse object
        """
        response = self.airship.request(
            method="POST",
            body=json.dumps(self.payload).encode("UTF-8"),
            url=self.airship.urls.get("attributes_url"),
            version=3,
        )

        return AttributeResponse(response=response)


class AttributeList(object):
    """
    Define and manage attribute lists; upload corresponding attribute data in CSV format.

    :param airship: Required. An unbanairship.Airship instance.
    :param list_name: Required. The name of your list. Must be prefixed
        with ``ua_attributes_``
    :param description: Required. A description of your list.
    :param extra: Optional. An optional dict of up to 100 key-value (string-to-string)
        pairs associated with the list.
    """

    def __init__(
        self,
        airship: Airship,
        list_name: str,
        description: str,
        extra: Optional[Dict[str, str]] = None,
    ):
        self.airship = airship
        self.list_name = list_name
        self.description = description
        self.extra = extra

    @property
    def _create_payload(self) -> Dict:
        payload: Dict = {"name": self.list_name, "description": self.description}

        if self.extra:
            payload["extra"] = self.extra

        return payload

    def create(self) -> Response:
        """Create the Attribute List"""
        response = self.airship.request(
            method="POST",
            url=self.airship.urls.get("attributes_list_url"),
            body=json.dumps(self._create_payload),
            content_type="application/json",
            version=3,
        )

        return response

    def upload(self, file_path: str) -> Response:
        """
        Upload a CSV that will set attribute values on the specified channels or
        named users. Please see the documentation at
        https://docs.airship.com/api/ua/#operation-api-attribute-lists-list_name-csv-put
        for details about list formatting, size limits, and error responses.

        :param file_path: Required. Local path to the csv file to be uploaded.
        """
        with open(file_path, "rb") as open_file:
            response = self.airship._request(
                method="PUT",
                body=GzipCompressReadStream(open_file),
                url=self.airship.urls.get("attributes_list_url")
                + self.list_name
                + "/csv/",
                content_type="text/csv",
                version=3,
                encoding="gzip",
            )

        return response

    def get_errors(self) -> Response:
        """
        Returns csv of attribute list processing errors. During processing, after a
        list is uploaded, errors can occur. Depending on the type of list
        processing, an error file may be created, showing a user exactly what
        went wrong.
        """
        response = self.airship.request(
            method="GET",
            body={},
            url=self.airship.urls.get("attributes_list_url")
            + self.list_name
            + "/errors/",
        )

        return response

    @classmethod
    def list(cls, airship: Airship) -> Response:
        """Lists existing attribute lists.

        :param airship: An urbanairship.Airship instance.
        """
        response = airship._request(
            method="GET",
            url=airship.urls.get("attributes_list_url"),
            body={},
            version=3,
        )

        return response
