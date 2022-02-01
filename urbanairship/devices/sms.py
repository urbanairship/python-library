from datetime import datetime
import json
import logging
import re
from typing import Dict, Optional, List, Union, Any

from requests import Response

from urbanairship import Airship

logger = logging.getLogger("urbanairship")

VALID_MSISDN = re.compile(r"[0-9]*$")
VALID_SENDER = re.compile(r"[0-9]*$")


class Sms(object):
    """
    Create, register, opt-out and uninstall an Sms object.

    :param airship: Required. An urbanairship.Airship object instantiated with
        master authentication.
    :param sender: Required. The a number that recipients will receive SMS
        notifications from. This must match your Urban Airship configuration.
    :param msisdn: Required. The mobile phone number you want to register as
        an SMS channel (or send a request to opt-in).
    :param opted_in: A datetime.datetime object that represents the
        date and time when explicit permission was received from the user to
        receive messages. This is required for use with CreateAndSend.
    :param template_fields: For use with CreateAndSend with inline templates.
        A dict of template field names and their substitution values.
    :param locale_country: The ISO 3166 two-character country code. The value for this
        field becomes a tag in the ua_locale_country tag group.
    :param locale_language: The ISO 639-1 two-character language code. The value for
        this field becomes a tag in the ua_locale_language tag group.
    :param timezone: The IANA identifier for a timezone, e.g. "America/Los_Angeles".
        The value in this field becomes a tag in the timezone tag group.
    """

    def __init__(
        self,
        airship: Airship,
        sender: str,
        msisdn: str,
        opted_in: Optional[datetime] = None,
        template_fields: Optional[Dict] = None,
        locale_country: Optional[str] = None,
        locale_language: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> None:
        self.airship = airship
        self.sender = sender
        self.msisdn = msisdn
        self.opted_in = opted_in
        self.template_fields = template_fields
        self.locale_country = locale_country
        self.locale_language = locale_language
        self.timezone = timezone
        self.channel_id = None

    @property
    def locale_country(self) -> Optional[str]:
        return self._locale_country

    @locale_country.setter
    def locale_country(self, value: Optional[str]) -> None:
        if not isinstance(value, (str, type(None))):
            raise ValueError("locale_country must be a 2 character string")

        self._locale_country = value

    @property
    def opted_in(self) -> Optional[datetime]:
        return self._opted_in

    @opted_in.setter
    def opted_in(self, value: Optional[datetime]) -> None:
        if not value:
            self._opted_in = None
            return

        self._opted_in = value

    @property
    def locale_language(self) -> Optional[str]:
        return self._locale_language

    @locale_language.setter
    def locale_language(self, value: Optional[str]) -> None:
        if not isinstance(value, (str, type(None))):
            raise ValueError("locale_language must be a 2 character string")

        self._locale_language = value

    @property
    def timezone(self) -> Optional[str]:
        return self._timezone

    @timezone.setter
    def timezone(self, value: Optional[str]) -> None:
        self._timezone = value

    @property
    def template_fields(self) -> Optional[Dict]:
        return self._template_fields

    @template_fields.setter
    def template_fields(self, value: Optional[Dict]):
        if not isinstance(value, (dict, type(None))):
            raise TypeError("template_fields must be a dict")

        self._template_fields = value

    @property
    def sender(self) -> str:
        return self._sender

    @sender.setter
    def sender(self, value: str) -> None:
        if not VALID_SENDER.match(value):
            raise ValueError("sender must be a numeric string")
        self._sender = value

    @property
    def msisdn(self) -> str:
        return self._msisdn

    @msisdn.setter
    def msisdn(self, value: str) -> None:
        if not VALID_MSISDN.match(value):
            raise ValueError("msisdn must be a numeric string")
        self._msisdn = value

    @property
    def common_payload(self) -> Dict:
        return {"sender": self.sender, "msisdn": self.msisdn}

    @property
    def _registration_payload(self) -> Dict:
        payload = self.common_payload

        reg_payload_keys = [
            "locale_language",
            "locale_country",
            "timezone",
            "template_fields",
            "opted_in",
        ]

        for key in reg_payload_keys:
            if getattr(self, key) is not None:
                if isinstance(getattr(self, key), datetime):
                    payload[key] = datetime.strptime(
                        getattr(self, key), "%Y-%m-%dT%H:%M:%S"
                    )
                else:
                    payload[key] = getattr(self, key)

        return payload

    @property
    def create_and_send_audience(self) -> Dict:
        audience: Dict[str, Any] = {"ua_sender": self.sender, "ua_msisdn": self.msisdn}

        if self.template_fields:
            audience.update(self.template_fields)

        if self.opted_in:
            audience["ua_opted_in"] = self.opted_in
        else:
            raise ValueError(
                "sms objects for create and send must include opt-in datestamps"
            )
        return audience

    def register(self, opted_in: Optional[datetime] = None) -> Response:
        """
        Register an Sms channel with the sender ID and MSISDN

        :param opted_in: Optional UTC ISO 8601 datetime string that represents the
            date and time when explicit permission was received from the
            user to receive messages.

        :return: The response object from the api.
        """

        if opted_in is not None:
            self.opted_in = opted_in

        url = self.airship.urls.get("sms_url")
        body = json.dumps(self._registration_payload)

        response = self.airship.request(method="POST", body=body, url=url, version=3)

        if response.json().get("status") == "pending":
            logger.info(
                "Channel creation for msisdn %s pending user opt-in" % (self.msisdn)
            )
        elif response.json().get("channel_id") is not None:
            self.channel_id = response.json().get("channel_id")
            logger.info(
                "Successfully registered Sms channel with channel_id %s"
                % (self.channel_id)
            )
        else:
            logger.info("Channel not yet created.")

        return response

    def update(self, channel_id: Optional[str] = None) -> Response:
        """
        Updates properties of an existing SMS channel.

        :param channel_id Optional: An existing airship-provided channel_id UUID for an SMS
            channel. If this object was created with this class, the channel_id value
            should be assigned. Otherwise, pass it here. Other values are set as
            properties on an instance of this class before the update call.

        :return: The response object from the API
        """

        if self.channel_id is None:
            raise ValueError("SMS Channel must have a channel id to update.")

        self.channel_id = channel_id

        response = self.airship.request(
            method="PUT",
            body=json.dumps(self._registration_payload).encode("utf-8"),
            url=self.airship.urls.get("sms_url") + self.channel_id,
            version=3,
        )

        return response

    def opt_out(self) -> Response:
        """
        Mark an sms channel at opted-out by sender ID and MSISDN

        :return: the response object from the api
        """

        url = self.airship.urls.get("sms_opt_out_url")

        response = self.airship.request(
            method="POST",
            body=json.dumps(self.common_payload).encode("utf-8"),
            url=url,
            version=3,
        )

        logger.info(
            "Opted out Sms channel with sender: %s and msisdn: %s"
            % (self.sender, self.msisdn)
        )

        return response

    def uninstall(self) -> Response:
        """
        Uninstall and remove all associated data from Airship
        systems. Channel cannot be opted-in again. Use with caution.

        :return: the response object from the api"""

        url = self.airship.urls.get("sms_uninstall_url")

        response = self.airship.request(
            method="POST",
            body=json.dumps(self.common_payload).encode("utf-8"),
            url=url,
            version=3,
        )

        logger.info(
            "Uninstalled Sms channel with sender: %s and msisdn: %s"
            % (self.sender, self.msisdn)
        )

        return response

    def lookup(self) -> Response:
        """
        Look up Sms channel information

        :return: the response object from the api
        """

        url = self.airship.urls.get("sms_url") + "{msisdn}/{sender}".format(
            msisdn=self.msisdn, sender=self.sender
        )

        response = self.airship.request(method="GET", body=None, url=url, version=3)

        return response


class KeywordInteraction(object):
    """
    Trigger Mobile Originated (MO) keyword interactions on behalf of an MSISDN.

    :param airship: Required. An urbanairship.Airship instance.
    :param keyword: Required. The keyword to use for the interaction.
    :param msisdn: Required. The MSISDN to use for the interacton.
    :param sender_ids: Required. A list of sender id values to use for the interaction.
    :param timestamp: Optional. A datetime.datetime representing the time of the interaction.
    """

    def __init__(
        self,
        airship: Airship,
        keyword: str,
        msisdn: str,
        sender_ids: List[str],
        timestamp: Optional[datetime] = None,
    ) -> None:
        self.airship = airship
        self.keyword = keyword
        self.msisdn = msisdn
        self.sender_ids = sender_ids
        self.timestamp = timestamp

        if type(sender_ids) is not list:
            raise ValueError("sender_ids must be a list")

    @property
    def timestamp(self) -> Optional[datetime]:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: Optional[datetime]) -> None:
        if type(value) is not datetime and value is not None:
            raise ValueError("timestamp must be a datetime object")

        self._timestamp = value

    @property
    def payload(self) -> Dict:
        data: Dict = {"keyword": self.keyword, "sender_ids": self.sender_ids}
        if self.timestamp:
            data.update(
                {"timestamp": self.timestamp.replace(microsecond=0).isoformat()}
            )

        return data

    @property
    def url(self) -> str:
        return "{base_url}sms/{msisdn}/keywords".format(
            base_url=self.airship.urls.get("base_url"), msisdn=self.msisdn
        )

    def post(self) -> Response:
        """Send the interaction"""
        response = self.airship.request(
            method="POST", url=self.url, body=self.payload, version=3
        )

        return response


class SmsCustomResponse:
    """Respond to a mobile originated message based on a keyword consumed by your
    custom response webhook, using a mobile-originated ID. Please see the documentation
    at https://docs.airship.com/api/ua/?http#operation-api-sms-custom-response-post for
    details on use of this feature.

    One of `mms` or `sms` is required.

    :param airship: [required] An urbanairship.Airship instance, created with
        bearer token authentication.
    :param mobile_originated_id: [required] The identifier that you received through
        your SMS webhook corresponding to the mobile-originated message that you're
        issuing a custom response to.
    :param sms: [optional] An SMS platform override object, created using
        `ua.sms()`. This defines the message sent in response.
    :param mms: [optional] An MMS platform override object, created using
        `us.mms()`. The defines the message sent in response.
    """

    def __init__(
        self,
        airship: Airship,
        mobile_originated_id: str,
        sms: Optional[Dict] = None,
        mms: Optional[Dict] = None,
    ) -> None:
        self.airship = airship
        self.mobile_originated_id = mobile_originated_id
        self.sms = sms
        self.mms = mms

    @property
    def sms(self) -> Optional[Dict]:
        return self._sms

    @sms.setter
    def sms(self, value: Optional[Dict]) -> None:
        self._sms = value

    @property
    def mms(self) -> Optional[Dict]:
        return self._mms

    @mms.setter
    def mms(self, value: Optional[Dict]) -> None:
        self._mms = value

    @property
    def _payload(self) -> Dict:
        if all((self.mms, self.sms)):
            raise ValueError("Cannot use both mms and sms.")
        if all((self.sms is None, self.mms is None)):
            raise ValueError("One of mms or sms must be set.")

        payload: Dict[str, Any] = {"mobile_originated_id": self.mobile_originated_id}

        if self.sms is not None:
            payload["sms"] = self.sms
        if self.mms is not None:
            payload.update(self.mms)

        return payload

    def send(self) -> Dict:
        """Sends the response using the mobile_originated_id value

        :return: An API response dictionary
        """
        response = self.airship.request(
            method="POST",
            body=json.dumps(self._payload),
            url=self.airship.urls.get("sms_custom_response_url"),
            content_type="application/json",
            version=3,
        )

        return response.json()
