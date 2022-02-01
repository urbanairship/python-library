import base64
import json
import logging
import re
from typing import Any, Dict, List, Optional

from requests import Response

from urbanairship import Airship

logger = logging.getLogger("urbanairship")

VALID_EMAIL = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
VALID_ISO_8601 = re.compile(
    "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])"
    "T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z)?$"
)


class Email(object):
    """Register and uninstall an Email object.

    Please see the email documentation for important information about
    opt-in times and email types.
    hhttps://docs.airship.com/api/ua/#tag-email

    :param address: Required. The email address the object represents.
    :param commercial_opted_in: Optional. A string in ISO 8601 format that
        represents the time explicit permission was received from the user
        to accept commercial emails.
    :param commercial_opted_out: Optional. A string in ISO 8601 format that
        represents the time a user opted out of commercial emails.
    :param transactional_opted_in: Optional. A string in ISO 8601 format
        that represents the time a user explicitly opted in to transactional
        emails.
    :param transactional_opted_out: Optional. A string in ISO 8601 formation
        that represents the time a user explicitly opted out of transactional
        emails.
    :param locale_country: Optional. The device property tag related
        to locale country setting.
    :param locale_language: Optional. The device property tag related
        to locale language setting.
    :param opt_in_mode: Optional. The opt-in mode for registering the channel. `classic`
        is the default when unspecified, `double` creates a `double_opt_in` event.
    :param properties: Optional. An object containing event properties. You can use
        these properties to filter the double opt-in event and reference them in your
        message content by using handlebars. Items in the `properties` object are
        limited to a 255-character maximum string length.
    :param timezone: Optional. The deice property tag related to
        timezone setting.
    :param template_fields: For use with CreateAndSend with inline templates.
        A dict of template field names and their substitution values.
    """

    def __init__(
        self,
        airship: Airship,
        address: str,
        commercial_opted_in: Optional[str] = None,
        commercial_opted_out: Optional[str] = None,
        transactional_opted_in: Optional[str] = None,
        transactional_opted_out: Optional[str] = None,
        locale_country: Optional[str] = None,
        locale_language: Optional[str] = None,
        opt_in_mode: Optional[str] = None,
        properties: Optional[Dict] = None,
        timezone: Optional[str] = None,
        template_fields: Optional[Dict] = None,
    ) -> None:
        self.airship = airship
        self.address = address
        self.commercial_opted_in = commercial_opted_in
        self.commercial_opted_out = commercial_opted_out
        self.transactional_opted_in = transactional_opted_in
        self.transactional_opted_out = transactional_opted_out
        self.locale_country = locale_country
        self.locale_language = locale_language
        self.opt_in_mode = opt_in_mode
        self.properties = properties
        self.timezone = timezone
        self.template_fields = template_fields
        self._email_type = "email"  # only acceptable value at this time
        self.channel_id: Optional[str] = None

    @property
    def template_fields(self) -> Optional[Dict]:
        return self._template_fields

    @template_fields.setter
    def template_fields(self, value: Optional[Dict]) -> None:
        if not isinstance(value, (dict, type(None))):
            raise TypeError("template_fields must be a dict")

        self._template_fields = value

    @property
    def opt_in_mode(self) -> Optional[str]:
        return self._opt_in_mode

    @opt_in_mode.setter
    def opt_in_mode(self, value: Optional[str]) -> None:
        if value not in ["classic", "double"] and value is not None:
            raise ValueError("opt_in_mode must be one of: 'classic' or 'double'")

        self._opt_in_mode = value

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        if not VALID_EMAIL.match(value) and value is not None:
            raise ValueError("Invalid email address")
        self._address = value

    @property
    def commercial_opted_in(self) -> Optional[str]:
        return self._commercial_opted_in

    @commercial_opted_in.setter
    def commercial_opted_in(self, value: Optional[str]) -> None:
        if value is not None and not VALID_ISO_8601.match(value):
            raise ValueError("Must use ISO 8601 timestamp format")
        self._commercial_opted_in = value

    @property
    def commercial_opted_out(self) -> Optional[str]:
        return self._commercial_opted_out

    @commercial_opted_out.setter
    def commercial_opted_out(self, value: Optional[str]) -> None:
        if value is not None and not VALID_ISO_8601.match(value):
            raise ValueError("Must use ISO 8601 timestamp format")
        self._commercial_opted_out = value

    @property
    def transactional_opted_in(self) -> Optional[str]:
        return self._transactional_opted_in

    @transactional_opted_in.setter
    def transactional_opted_in(self, value: Optional[str]) -> None:
        if value is not None and not VALID_ISO_8601.match(value):
            raise ValueError("Must use ISO 8601 timestamp format")
        self._transactional_opted_in = value

    @property
    def transactional_opted_out(self) -> Optional[str]:
        return self._transactional_opted_out

    @transactional_opted_out.setter
    def transactional_opted_out(self, value: Optional[str]) -> None:
        if value is not None and not VALID_ISO_8601.match(value):
            raise ValueError("Must use ISO 8601 timestamp format")
        self._transactional_opted_out = value

    @property
    def _full_payload(self) -> Dict[str, Any]:
        if self.address == None:
            raise ValueError(
                "address must be set to register or update an email channel"
            )

        payload: Dict[str, Any] = {"type": self._email_type}

        reg_payload_keys = [
            "address",
            "commercial_opted_in",
            "commercial_opted_out",
            "locale_country",
            "locale_language",
            "opt_in_mode",
            "properties",
            "timezone",
            "transactional_opted_in",
            "transactional_opted_out",
        ]

        for key in reg_payload_keys:
            if getattr(self, key) is not None:
                payload[key] = getattr(self, key)

        return payload

    @property
    def _registration_payload(self) -> Dict:
        full_payload = self._full_payload
        opt_in_mode = full_payload.pop("opt_in_mode", None)
        properties = full_payload.pop("properties", None)

        payload = {"channel": full_payload}
        if opt_in_mode:
            payload["opt_in_mode"] = opt_in_mode
        if properties:
            payload["properties"] = properties

        return payload

    @property
    def _update_payload(self) -> Dict:
        payload = self._full_payload

        payload.pop("opt_in_mode", None)
        payload.pop("properties", None)

        return {"channel": payload}

    @property
    def create_and_send_audience(self) -> Dict:
        audience = {"ua_address": self.address}
        if self.commercial_opted_in:
            audience["ua_commercial_opted_in"] = self.commercial_opted_in
        if self.transactional_opted_in:
            audience["ua_transactional_opted_in"] = self.transactional_opted_in
        if self.template_fields:
            audience.update(self.template_fields)

        return audience

    def register(self) -> Response:
        """Create a new email channel or unsubscribe an existing email
        channel from receiving commercial emails.
        To unsubscribe an existing channel, set email_opt_in_level
        to none.

        :return: The response object from the API.
        """
        url = self.airship.urls.get("email_url")

        response = self.airship.request(
            method="POST",
            body=json.dumps(self._registration_payload).encode("utf-8"),
            url=url,
            version=3,
        )

        if response.status_code == 201:
            self.channel_id = response.json().get("channel_id")
            logger.info(
                "Successfully created channel with channel_id %s" % (self.channel_id)
            )
        elif response.status_code == 200:
            self.channel_id = response.json().get("channel_id")
            logger.info(
                "Successful registration call made to channel_id %s" % (self.channel_id)
            )

        return response

    def update(self, channel_id: Optional[str] = None) -> Response:
        """
        Updates an existing email channel.

        :param channel_id Optional: An existing airship-provided channel_id UUID for an
            email channel.
            If this object was created with this class, the channel_id value
            should be assigned. Otherwise, pass it here. Other values are set as
            properties on an instance of this class before the update call.
        """
        if channel_id:
            self.channel_id = channel_id

        if self.channel_id is None:
            raise ValueError("Email channel must have a channel_id to update.")

        response = self.airship.request(
            method="PUT",
            body=json.dumps(self._update_payload),
            url=self.airship.urls.get("email_url") + self.channel_id,
            version=3,
        )

        return response

    def uninstall(self) -> Response:
        """Removes an email address from Urban Airship. Use with caution.
        If the uninstalled email address opts-in again, it will generate
        a new channel_id.
        The new channel_id cannot be reassociated with any opt-in
        information, tags, named users, insight reports, or other
        information from the uninstalled email channel.

        :return: The response object from the API"""

        url = self.airship.urls.get("email_uninstall_url")
        uninstall_payload = {"email_address": self.address}

        body = json.dumps(uninstall_payload).encode("utf-8")

        response = self.airship.request(method="POST", body=body, url=url, version=3)

        logger.info("Uninstalled email address: %s" % self.address)

        return response

    @classmethod
    def lookup(cls, airship: Airship, address: str) -> Response:
        if not VALID_EMAIL.match(address) and address is not None:
            raise ValueError("Invalid email address format")

        url = airship.urls.get("email_url") + address

        response = airship.request(method="GET", url=url, version=3, body=None)

        return response


class EmailTags(object):
    """Add, remove or set tags for a list of email addresses

    :param address: an email address to mutate tags for
    """

    def __init__(self, airship: Airship, address: str):
        self.airship = airship
        self.url = airship.urls.get("email_tags_url")
        self.address = address
        self.add_group: Dict[str, Any] = {}
        self.remove_group: Dict[str, Any] = {}
        self.set_group: Dict[str, Any] = {}
        self._payload: Dict[str, Any] = {}

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        if not VALID_EMAIL.match(value):
            raise ValueError("addresses must be and email address")
        self._address = value

    @property
    def tags(self) -> List[str]:
        return self._tags

    @tags.setter
    def tags(self, value: List[str]) -> None:
        if not isinstance(value, list):
            raise ValueError("tags must be input as a list")
        self._tags = value

    def add(self, group: str, tags: List[str]) -> None:
        """
        add tags to a given tag group
        :param group: the tag group to add to
        :param tags: a list of tags to add
        """
        self.add_group[group] = tags

    def remove(self, group: str, tags: List[str]) -> None:
        """
        remove tags from a given tag group
        :param group: the tag group to remove tags from
        :param tags: a list of tags to remove
        """
        self.remove_group[group] = tags

    def set(self, group: str, tags: List[str]) -> None:
        """
        replace all tags on the given tag group with these tags
        :param group: the tag group to set tags on
        :param tags: a list of tags to set
        """
        self.set_group[group] = tags

    def send(self) -> Response:
        """
        commit add, remove and set operations. set cannot be used with
        add and remove.

        :return: the response object from the api
        """
        if not self.add_group and not self.remove_group and not self.set_group:
            raise ValueError("at least one add, remove or set group must exist")
        self._payload["audience"] = {"email_address": self.address}

        if self.set_group:
            if self.add_group or self.remove_group:
                raise ValueError("set cannot be used with remove or add groups")
            self._payload["set"] = self.set_group

        if self.add_group:
            self._payload["add"] = self.add_group

        if self.remove_group:
            self._payload["remove"] = self.remove_group

        body = json.dumps(self._payload).encode("utf-8")

        response = self.airship.request(
            method="POST", body=body, url=self.url, version=3
        )

        return response


class EmailAttachment(object):
    """
    Create an email attachment from a file.
    Please see https://docs.airship.com/api/ua/#operation/api/attachments/post
    for important information about file size, content type, and send type limitations.

    :param filename: Required. The name of the uploaded file (max 255 UTF-8 bytes).
        Multiple files with the same name are allowed in separate requests.
    :param content_type: Required: The mimetype of the uploaded file including the
        charset parameter, if needed.
    :param filepath: Required. A path to the file to be uploaded and attached. File must
        have permissions set to be opened in 'rb' (binary) mode.

    :return: the response object from the API including the 'attachment_ids' uuid to
        be used in the email override object.
    """

    def __init__(
        self, airship: Airship, filename: str, content_type: str, filepath: str
    ) -> None:
        self.airship = airship
        self.filename = filename
        self.content_type = content_type
        self.filepath = filepath

    def _encode_attachment(self, filepath: str) -> str:
        file = open(filepath, "rb").read()
        enc = base64.urlsafe_b64encode(file)

        return str(enc)

    @property
    def req_payload(self) -> Dict:
        attachment_payload = {
            "filename": self.filename,
            "content_type": self.content_type,
            "data": self._encode_attachment(self.filepath),
        }

        return attachment_payload

    def post(self) -> Dict:
        response = self.airship.request(
            method="POST",
            body=json.dumps(self.req_payload),
            url=self.airship.urls.get("attachment_url"),
            content_type="application/json",
            version=3,
        )

        return response.json()
