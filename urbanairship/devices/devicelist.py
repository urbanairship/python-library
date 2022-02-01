import datetime
import logging
from typing import Any, Dict, Optional, List, Generic, TypeVar

from urbanairship import common, Airship

logger = logging.getLogger("urbanairship")

ChannelInfoType = TypeVar("ChannelInfoType", bound="ChannelInfo")


class ChannelInfo(object):
    """Information object for iOS, Android, Amazon, web, and open channels.

    :keyword address: Replaces ``push_address`` for open channels.
    :keyword alias: Alias associated with this device, if any.
    :keyword background: Bool; whether the device is opted in to background push.
    :keyword channel_id: Channel ID for the device.
    :keyword created: UTC datetime when the system initially saw the device.
    :keyword device_type: Type of the device, e.g. ``ios``.
    :keyword installed: Bool; whether the app is installed on the device.
    :keyword last_registration: UTC datetime when the system last received a
        registration call for the device.
    :keyword named_user_id: Named user associated with this device, if any.
    :keyword opt_in: Bool; whether the device is opted in to push or other visible
        notifications.
    :keyword push_address: Address we use to push to the device (device token,
        GCM registration ID, etc,). Not present for open channels (see
        ``address`` above).
    :keyword tag_groups: Tags associated with non-"device" tag groups, if any.
    :keyword tags: List of tags associated with this device, if any.
    :keyword ios: iOS specific information, e.g. ``badge`` and ``quiet_time``.
    :keyword open: Open channel specific information, e.g. ``identifiers`` and
        ``open_platform_name``.
    :keyword web: Web notify specific information, e.g. ``subscription``.
    :keyword named_user_id: A customer-chosen ID that represents the device user.
    :keyword device_attributes: Native attribute properties that Airship gathers
        automatically assigns to a channel. Varies by channel type.
    :keyword attributes: A dictionary of attributes that you've associated with the
        channel.
    :keyword commercial_opted_in: The date-time when a user gave explicit permission
        to receive commercial emails.
    :keyword commcercial_opted_out: The date-time when a user explicitly denied permission
        to receive commercial emails.
    :keyword transactional_opted_in: The date-time when a user gave explicit permission to
        receive transactional emails. Users do not need to opt-in to receive
        transactional emails unless they have previously opted out.
    :keyword transactional_opted_out: The date-time when a user explicitly denied
        permission to receive transactional emails.
    """

    address: Optional[str] = None
    alias: Optional[str] = None
    background: Optional[bool] = None
    channel_id: Optional[str] = None
    created: Optional[str] = None
    device_type: Optional[str] = None
    installed: Optional[bool] = None
    last_registration: Optional[str] = None
    opt_in: Optional[bool] = None
    push_address: Optional[str] = None
    tag_groups: Optional[str] = None
    tags: Optional[List] = None
    ios: Optional[Dict] = None
    open: Optional[Dict] = None
    web: Optional[Dict] = None
    named_user_id: Optional[str] = None
    device_attributes: Optional[Dict] = None
    attributes: Optional[Dict] = None
    commercial_opted_in: Optional[str] = None
    commercial_opted_out: Optional[str] = None
    transactional_opted_in: Optional[str] = None
    transactional_opted_out: Optional[str] = None

    def __init__(self, airship):
        self.airship = airship

    @classmethod
    def from_payload(cls, payload: Dict, device_key: str, airship: Airship):
        """Create based on results from a ChannelList iterator."""
        obj = cls(airship)
        obj.channel_id = payload[device_key]
        if airship:
            obj.airship = airship
        for key in payload:
            if key in (
                "created",
                "last_registration",
                "commercial_opted_in",
                "commercial_opted_out",
                "transactional_opted_in",
                "transactional_opted_out",
            ):
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], "%Y-%m-%dT%H:%M:%S"
                    )
                except:
                    payload[key] = "UNKNOWN"
            setattr(obj, key, payload[key])
        return obj

    def lookup(self, channel_id: str):
        """Fetch metadata from a channel ID"""
        start_url = self.airship.urls.get("channel_url")
        data_attribute = "channel"
        id_key = "channel_id"
        params: Dict[str, Any] = {}
        url = start_url + channel_id
        response = self.airship._request(
            method="GET", body=None, url=url, version=3, params=params
        )
        payload = response.json()
        return self.from_payload(payload[data_attribute], id_key, self.airship)


class DeviceInfo(object):
    """Information object for a single device.

    :keyword active: bool; Whether the device is opted in to push or other visible
        notifications.
    :keyword alias: Alias associated with this device, if any.
    :keyword created: UTC datetime when the system initially saw the device.
    :keyword device_type: Type of the device, e.g. ``device_token``, ``apid``.
    :keyword id: Device identifier. Also available at the attribute named by the
        ``device_type``.
    :keyword tags: List of tags associated with this device, if any.
    :keyword apid: Same as device identifier if apid device type.
    :keyword device_token: Same as device identifier if device_token device type.

    """

    id: Optional[str] = None
    device_type: Optional[str] = None
    active: Optional[bool] = None
    tags: Optional[List] = None
    alias: Optional[str] = None

    def __init__(self, airship: Airship):
        self.airship = airship

    @classmethod
    def from_payload(cls, payload: Dict, device_key: str, airship: Airship):
        """Create based on results from a DeviceTokenList or APIDList iterator."""
        obj = cls(airship)
        obj.id = payload[device_key]
        obj.device_type = device_key
        for key in payload:
            if key in "created":
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], "%Y-%m-%d %H:%M:%S"
                    )
                except:
                    payload[key] = "UNKNOWN"
            setattr(obj, key, payload[key])
        return obj


class DeviceTokenList(common.IteratorParent):
    """Iterator for listing all device tokens for this application.

    :keyword limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """

    next_url: Optional[str] = None
    data_attribute: str = "device_tokens"
    id_key: str = "device_token"
    instance_class = DeviceInfo

    def __init__(self, airship, limit=None):
        self.next_url = airship.urls.get("device_token_url")
        params = {"limit": limit} if limit else {}
        super(DeviceTokenList, self).__init__(airship, params)


class ChannelList(common.IteratorParent):
    """Iterator for listing all channels for this application.

    :keyword limit: Number of entries to fetch in each page request.
    :keyword start_channel: uuid representing the channel_id to start with.
    :returns: Each ``next`` returns a :py:class:`ChannelInfo` object.

    """

    next_url: Optional[str] = None
    data_attribute: str = "channels"
    id_key: str = "channel_id"
    instance_class = ChannelInfo

    def __init__(self, airship, limit=None, start_channel=None):
        self.next_url = airship.urls.get("channel_url")
        channel_params = {}
        if limit:
            channel_params["limit"] = limit
        if start_channel:
            channel_params["start"] = start_channel

        super(ChannelList, self).__init__(airship, params=channel_params)


class APIDList(common.IteratorParent):
    """Iterator for listing all APIDs for this application.

    :keyword limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """

    next_url: Optional[str] = None
    data_attribute: str = "apids"
    id_key: str = "apid"
    instance_class = DeviceInfo

    def __init__(self, airship, limit=None):
        self.next_url = airship.urls.get("apid_url")
        params = {"limit": limit} if limit else {}
        super(APIDList, self).__init__(airship, params)
