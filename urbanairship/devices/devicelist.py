import datetime
import logging
from urbanairship import common

logger = logging.getLogger('urbanairship')


class ChannelInfo(object):
    """Information object for iOS, Android, Amazon, web, and open channels.

    :ivar address: Replaces ``push_address`` for open channels.
    :ivar alias: Alias associated with this device, if any.
    :ivar background: Bool; whether the device is opted in to background push.
    :ivar channel_id: Channel ID for the device.
    :ivar created: UTC datetime when the system initially saw the device.
    :ivar device_type: Type of the device, e.g. ``ios``.
    :ivar installed: Bool; whether the app is installed on the device.
    :ivar last_registration: UTC datetime when the system last received a
        registration call for the device.
    :ivar named_user_id: Named user associated with this device, if any.
    :ivar opt_in: Bool; whether the device is opted in to push or other visible
        notifications.
    :ivar push_address: Address we use to push to the device (device token,
        GCM registration ID, etc,). Not present for open channels (see
        ``address`` above).
    :ivar tag_groups: Tags associated with non-"device" tag groups, if any.
    :ivar tags: List of tags associated with this device, if any.
    :ivar ios: iOS specific information, e.g. ``badge`` and ``quiet_time``.
    :ivar open: Open channel specific information, e.g. ``identifiers`` and
        ``open_platform_name``.
    :ivar web: Web notify specific information, e.g. ``subscription``.

    """

    airship = None
    address = None
    alias = None
    background = None
    channel_id = None
    created = None
    device_type = None
    installed = None
    last_registration = None
    opt_in = None
    push_address = None
    tag_groups = None
    tags = None
    ios = None
    open = None
    web = None

    def __init__(self, airship):
        self.airship = airship

    @classmethod
    def from_payload(cls, payload, device_key, airship):
        """Create based on results from a ChannelList iterator."""
        obj = cls(airship)
        obj.channel_id = payload[device_key]
        if airship:
            obj.airship = airship
        for key in payload:
            if key in ('created', 'last_registration'):
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], '%Y-%m-%dT%H:%M:%S'
                    )
                except:
                    payload[key] = 'UNKNOWN'
            setattr(obj, key, payload[key])
        return obj

    def lookup(self, channel_id):
        """Fetch metadata from a channel ID"""
        start_url = self.airship.urls.get('channel_url')
        data_attribute = 'channel'
        id_key = 'channel_id'
        params = {}
        url = start_url + channel_id
        response = self.airship._request(
            method='GET',
            body=None,
            url=url,
            version=3,
            params=params
        )
        payload = response.json()
        return self.from_payload(payload[data_attribute], id_key, self.airship)


class DeviceInfo(object):
    """Information object for a single device.

    :ivar active: bool; Whether the device is opted in to push or other visible
        notifications.
    :ivar alias: Alias associated with this device, if any.
    :ivar created: UTC datetime when the system initially saw the device.
    :ivar device_type: Type of the device, e.g. ``device_token``, ``apid``.
    :ivar id: Device identifier. Also available at the attribute named by the
        ``device_type``.
    :ivar tags: List of tags associated with this device, if any.
    :ivar apid: Same as device identifier if apid device type.
    :ivar device_token: Same as device identifier if device_token device type.

    """

    id = None
    device_type = None
    active = None
    tags = None
    alias = None

    def __init__(self, airship):
        self.airship = airship

    @classmethod
    def from_payload(cls, payload, device_key, airship):
        """Create based on results from a DeviceTokenList or APIDList iterator.

        """
        obj = cls(airship)
        obj.id = payload[device_key]
        obj.device_type = device_key
        for key in payload:
            if key in 'created':
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], '%Y-%m-%d %H:%M:%S'
                    )
                except:
                    payload[key] = 'UNKNOWN'
            setattr(obj, key, payload[key])
        return obj


class DeviceTokenList(common.IteratorParent):
    """Iterator for listing all device tokens for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    next_url = None
    data_attribute = 'device_tokens'
    id_key = 'device_token'
    instance_class = DeviceInfo

    def __init__(self, airship, limit=None):
        self.next_url = airship.urls.get('device_token_url')
        params = {'limit': limit} if limit else {}
        super(DeviceTokenList, self).__init__(airship, params)


class ChannelList(common.IteratorParent):
    """Iterator for listing all channels for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :ivar start_channel: uuid representing the channel_id to start with.
    :returns: Each ``next`` returns a :py:class:`ChannelInfo` object.

    """

    next_url = None
    data_attribute = 'channels'
    id_key = 'channel_id'
    instance_class = ChannelInfo

    def __init__(self, airship, limit=None, start_channel=None):
        self.next_url = airship.urls.get('channel_url')
        channel_params = {}
        if limit:
            channel_params['limit'] = limit
        if start_channel:
            channel_params['start'] = start_channel

        super(ChannelList, self).__init__(airship, params=channel_params)


class APIDList(common.IteratorParent):
    """Iterator for listing all APIDs for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    next_url = None
    data_attribute = 'apids'
    id_key = 'apid'
    instance_class = DeviceInfo

    def __init__(self, airship, limit=None):
        self.next_url = airship.urls.get('apid_url')
        params = {'limit': limit} if limit else {}
        super(APIDList, self).__init__(airship, params)
