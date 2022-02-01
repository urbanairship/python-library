import json
from lib2to3.pgen2.token import OP
import logging
import warnings
from typing import Any, Dict, Optional, List, Union

from requests import Response

from urbanairship import Airship, devices


logger = logging.getLogger("urbanairship")


class PushResponse(object):
    """Response to a successful push notification send or schedule.

    Right now this is a fairly simple wrapper around the json payload response,
    but making it an object gives us some flexibility to add functionality
    later.

    """

    ok: Optional[bool] = None
    localized_ids: Optional[List] = None
    push_ids: Optional[List] = None
    schedule_url: Optional[str] = None
    operation_id: Optional[str] = None
    payload: Optional[Dict] = None

    def __init__(self, response: Response):
        data = response.json()
        self.localized_ids = data.get("localized_ids", [])
        self.push_ids = data.get("push_ids")
        self.schedule_url = data.get("schedule_urls", [])
        self.operation_id = data.get("operation_id")
        self.ok = data.get("ok")
        self.payload = data

    def __str__(self) -> str:
        return "Response Payload: {0}".format(self.payload)


class Push(object):
    """A push notification. Set audience, message, etc, and send."""

    def __init__(self, airship: Airship) -> None:
        self._airship = airship
        self.audience: Optional[Union[Dict, List[Dict]]] = None
        self.notification: Optional[Dict[str, Any]] = None
        self.options: Optional[Dict[str, Any]] = None
        self.campaigns: Optional[Dict[str, Any]] = None
        self.message: Optional[Dict[str, Any]] = None
        self.in_app: Optional[Dict[str, Any]] = None
        self.localizations: Optional[Dict[str, Any]] = None

    @property
    def payload(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "audience": self.audience,
            "notification": self.notification,
            "device_types": self.device_types,
        }
        if self.options is not None:
            data["options"] = self.options
        if self.campaigns is not None:
            data["campaigns"] = self.campaigns
        if self.message is not None:
            data["message"] = self.message
        if self.in_app is not None:
            data["in_app"] = self.in_app
        if self.localizations is not None:
            data["localizations"] = self.localizations
        return data

    @property
    def device_types(self) -> List:
        return self._device_types

    @device_types.setter
    def device_types(self, types: List) -> None:
        self._device_types = types

    def validate(self) -> PushResponse:
        """
        Test push payload against the validate endpoint. No sends will result from this
        method being called. This method is otherwise identical to the `send` method.
        """

        response = self._airship._request(
            method="POST",
            body=json.dumps(self.payload),
            url=self._airship.urls.get("validate_url"),
            content_type="application/json",
            version=3,
        )

        return PushResponse(response)

    def send(self) -> PushResponse:
        """Send the notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.
        :raises ValueError: Required keys missing or incorrect values included.
        """
        if "email" in self.payload["notification"]:
            if self.payload["device_types"] == "all":
                raise ValueError(
                    "device_types cannot be all when including an email override"
                )
            if "email" not in self.payload["device_types"]:
                raise ValueError(
                    "email must be in device_types if email override is included"
                )
        if (
            "email" in self.payload["device_types"]
            and "email" not in self.payload["notification"]
        ):
            raise ValueError(
                "email override must be included when email is in device_types"
            )

        body = json.dumps(self.payload)
        response = self._airship._request(
            method="POST",
            body=body,
            url=self._airship.urls.get("push_url"),
            content_type="application/json",
            version=3,
        )

        data = response.json()
        logger.info(
            "Push successful. push_ids: %s", ", ".join(data.get("push_ids", []))
        )

        return PushResponse(response)

    @classmethod
    def message_center_delete(cls, airship: Airship, push_id: str) -> Response:
        """
        Delete a Message Center message completely, removing it from every user's inbox.
        This is an asynchronous call; a success response means that the deletion has
        been queued for processing.
        This delete call will work with either the message_id or the push_id of the
        accompanying push notification.
        This endpoint will not work with a group_id from an automated message or a
        push to local time delivery. To delete a rich message that was part of an
        automated or local time delivery, you must use the relevant push_id from the
        operation.

        :param airship: Required. Airship object instantiated with auth that corresponds
            to message to be deleted.
        :param push_id: Required. The message_id to delete or the push_id of the
            accompanying push notification.
        """

        response = airship._request(
            method="DELETE",
            url=airship.urls.get("message_center_delete_url") + push_id,
            body="",
            version=3,
        )

        return response


class ScheduledPush(object):
    """A scheduled push notification. Set schedule, push, and send."""

    def __init__(self, airship: Airship):
        self._airship = airship
        self.schedule: Optional[Dict[str, Any]] = None
        self.recurring: Optional[Dict[str, Any]] = None
        self.name: Optional[str] = None
        self.push: Optional[Push] = None
        self.url: Optional[str] = None

    @classmethod
    def from_url(cls, airship: Airship, url: str):
        """Load an existing scheduled push from its URL."""

        sched = cls(airship)
        response = sched._airship._request(method="GET", body=None, url=url, version=3)
        payload = response.json()
        sched.name = payload.get("name")
        sched.schedule = payload["schedule"]
        sched.push = Push(airship)
        sched.push.audience = payload["push"]["audience"]
        sched.push.notification = payload["push"]["notification"]
        sched.push.device_types = payload["push"]["device_types"]
        if "message" in payload["push"]:
            sched.push.message = payload["push"]["message"]
        if "options" in payload["push"]:
            sched.push.options = payload["push"]["options"]
        sched.url = url
        return sched

    @classmethod
    def from_payload(cls, payload: Dict, id_key: str, airship: Airship):
        """Create based on results from a ScheduledList iterator."""
        obj = cls(airship)
        for key in payload:
            setattr(obj, key, payload[key])
        return obj

    @property
    def payload(self) -> Dict:
        if not self.push:
            raise AttributeError("Must set push attribute to build payload.")
        if hasattr(self.push, "merge_data"):
            # create template payload
            data: Dict = self.push.payload
            data["schedule"] = self.schedule
        elif isinstance(self.push, CreateAndSendPush):  # create create and send payload
            if "scheduled_time" not in self.schedule:
                raise ValueError(
                    "only scheduled_time supported with create and send schedules"
                )
            data = {"schedule": self.schedule, "push": self.push.payload}
        else:
            data = {"schedule": self.schedule, "push": self.push.payload}

            if self.recurring:
                data["schedule"].update(self.recurring)

        if self.name is not None:
            data["name"] = self.name

        return data

    @property
    def api_url(self) -> str:
        if hasattr(self.push, "merge_data"):
            url = self._airship.urls.get("schedule_template_url")
        elif isinstance(self.push, CreateAndSendPush):
            url = self._airship.urls.get("schedule_create_and_send_url")
        else:
            url = self._airship.urls.get("schedules_url")

        return url

    def send(self) -> PushResponse:
        """Schedule the notification

        :returns: :py:class:`PushResponse` object with ``schedule_url`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """
        response = self._airship._request(
            method="POST",
            body=json.dumps(self.payload),
            url=self.api_url,
            content_type="application/json",
            version=3,
        )
        data = response.json()

        urls = data.get("schedule_urls", [])
        if urls:
            self.url = urls[0]
            logger.info(
                "Scheduled push successful. schedule_urls: %s",
                ", ".join(data.get("schedule_urls", [])),
            )

        else:
            logger.info("Scheduled push resulted in zero messages scheduled.")

        return PushResponse(response)

    def validate(self) -> PushResponse:
        """Validates a scheduled push for sending"""
        response = self._airship._request(
            method="POST",
            body=json.dumps(self.payload),
            url=self.api_url,
            content_type="application/json",
            version=3,
        )

        return PushResponse(response)

    def pause(self) -> Response:
        """Pause a recurring schedule"""
        if not self.url:
            raise ValueError("Cannot pause ScheduledPush without url.")

        response = self._airship._request(
            method="POST", body="", url=self.url + "/pause", version=3
        )

        return response

    def resume(self) -> Response:
        """Resume a paused recurring schedule"""
        if not self.url:
            raise ValueError("Cannot resume ScheduledPush without url.")

        response = self._airship._request(
            method="POST", body="", url=self.url + "/resume", version=3
        )

        return response

    def cancel(self) -> Response:
        """Cancel a previously scheduled notification."""
        if not self.url:
            raise ValueError("Cannot cancel ScheduledPush without url.")

        response = self._airship._request(
            method="DELETE", body=None, url=self.url, version=3
        )

        return response

    def update(self) -> PushResponse:
        if not self.url:
            raise ValueError("Cannot update ScheduledPush without url.")
        body = json.dumps(self.payload)
        response = self._airship._request(
            method="PUT",
            body=body,
            url=self.url,
            content_type="application/json",
            version=3,
        )

        data = response.json()
        logger.info(
            "Scheduled push update successful. schedule_urls: %s",
            ", ".join(data.get("schedule_urls", [])),
        )

        return PushResponse(response)


class TemplatePush(object):
    """A personalized push notification. Set details and send."""

    def __init__(self, airship):
        self._airship: Airship = airship
        self.audience: Optional[Dict] = None
        self.device_types: Optional[List] = None
        self.merge_data: Optional[Dict] = None

    @property
    def payload(self) -> Dict:
        data: Dict[str, Any] = {
            "audience": self.audience,
            "device_types": self.device_types,
            "merge_data": self.merge_data,
        }

        return data

    def send(self) -> PushResponse:
        """Send the personalized notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """

        if not self.audience:
            raise ValueError("Must set audience for template push.")

        if not self.device_types:
            raise ValueError("Must set device_types for template push.")

        body = json.dumps(self.payload)
        response = self._airship._request(
            method="POST",
            body=body,
            url=self._airship.urls.get("templates_url") + "push",
            content_type="application/json",
            version=3,
        )

        data = response.json()
        logger.info(
            "Push successful. push_ids: %s", ", ".join(data.get("push_ids", []))
        )

        return PushResponse(response)


class CreateAndSendPush(object):
    """
    Creates and sends to email, sms or open channels. Channel ids are created
    but not returned by this request. Use lookup/listing endpoints to find
    channel_id values. Opt-in date attributes are required on Sms and Email
    objects passed in.

    :param airship: Required. An urbanairship.Airship object instantiated with
        master authentication.
    :param channels: Required. A list of Sms, Email or OpenChannel objects.
        channels may only be of one type and must match the single value for
        CreateAndSend.device_types.
    """

    def __init__(self, airship: Airship, channels: List):
        self._airship = airship
        self.channels = channels
        self.notification: Optional[Dict] = None
        self.campaigns: Optional[Dict] = None

    @property
    def device_types(self) -> List[str]:
        return self._device_types

    @device_types.setter
    def device_types(self, values: List[str]):
        accepted_device_types = ("sms", "email", "open::")

        if len(values) != 1:
            raise ValueError("only a single device_type may be used.")

        for value in values:
            if value[:6] not in accepted_device_types:
                raise ValueError(
                    "device_types must be one of {}".format(str(accepted_device_types))
                )

        self._device_types = values

    @property
    def audience(self):
        if "email" in self.device_types:
            return self._email_audience()
        elif "sms" in self.device_types:
            return self._sms_audience()
        else:
            return self._open_channel_audience()

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, value):
        if type(value) is not list:
            raise TypeError("channels must be a list")
        if len(value) > 1000:
            raise ValueError("channels list must have 1000 or fewer items")

        self._channels = value

    @property
    def payload(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "audience": self.audience,
            "notification": self.notification,
            "device_types": self.device_types,
        }
        if self.campaigns is not None:
            data["campaigns"] = self.campaigns
        return data

    def _email_audience(self) -> Dict[str, Any]:
        addresses: List = []
        for email in self.channels:
            if not isinstance(email, devices.Email):
                raise TypeError(
                    "Can only use email channels when device_types is email"
                )
            addresses.append(email.create_and_send_audience)
        audience: Dict[str, Any] = {"create_and_send": addresses}

        return audience

    def _sms_audience(self) -> Dict[str, Any]:
        addresses: List = []
        for sms in self.channels:
            if not isinstance(sms, devices.Sms):
                raise TypeError("Can only use Sms objects when device_types is sms")
            addresses.append(sms.create_and_send_audience)
        audience: Dict[str, Any] = {"create_and_send": addresses}

        return audience

    def _open_channel_audience(self) -> Dict[str, Any]:
        addresses: List = []
        for open_channel in self.channels:
            if not isinstance(open_channel, devices.OpenChannel):
                raise TypeError(
                    "Can only use OpenChannel objects when device_types is open::"
                )
            addresses.append(open_channel.create_and_send_audience)
        audience: Dict[str, Any] = {"create_and_send": addresses}

        return audience

    def send(self) -> PushResponse:
        """Send the notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.
        :raises ValueError: Required keys missing or incorrect values included.
        """
        body = json.dumps(self.payload)
        response = self._airship._request(
            method="POST",
            body=body,
            url=self._airship.urls.get("create_and_send_url"),
            content_type="application/json",
            version=3,
        )

        logger.info("Create and Send successful")

        return PushResponse(response)
