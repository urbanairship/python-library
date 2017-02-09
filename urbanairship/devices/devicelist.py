import datetime
import json
import logging
from urbanairship import common

logger = logging.getLogger('urbanairship')


class ChannelInfo(object):
    """Information object for iOS, Android and Amazon device channels.

    :ivar channel_id: Channel ID for the device.
    :ivar device_type: Type of the device, e.g. ``ios``.
    :ivar installed: bool; whether the app is installed on the device.
    :ivar opt_in: bool; whether the device is opted in to push.
    :ivar background: bool; whether the device is opted in to background push.
    :ivar push_address: Address we use to push to the device (device token,
        GCM registration ID, etc,).
    :ivar created: UTC date and time the system initially saw the device.
    :ivar last_registration: UTC date and time the system last received a
        registration call for the device.
    :ivar tags: list of tags associated with this device, if any.
    :ivar alias: alias associated with this device, if any.
    :ivar ios: iOS specific information, e.g. ``badge``and ``quiet_time``.

    """

    channel_id = None
    device_type = None
    installed = None
    opt_in = None
    background = None
    push_address = None
    created = None
    last_registration = None
    tags = None
    alias = None
    ios = None

    @classmethod
    def from_payload(cls, payload, device_key):
        """Create based on results from a ChannelList iterator."""
        obj = cls()
        obj.channel_id = payload[device_key]
        for key in payload:
            if key in ('created', 'last_registration'):
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], '%Y-%m-%dT%H:%M:%S'
                    )
                except:
                    payload[key] = "UNKNOWN"
            setattr(obj, key, payload[key])
        return obj

    @classmethod
    def lookup(cls, airship, channel_id):
        """Fetch metadata from a channel ID"""
        start_url = common.CHANNEL_URL
        data_attribute = 'channel'
        id_key = 'channel_id'
        params = {}
        url = start_url + channel_id
        response = airship._request(
            method='GET',
            body=None,
            url=url,
            version=3,
            params=params
        )
        payload = response.json()
        return cls.from_payload(payload[data_attribute], id_key)


class DeviceTokenList(common.IteratorParent):
    """Iterator for listing all device tokens for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    next_url = common.DEVICE_TOKEN_URL
    data_attribute = 'device_tokens'
    id_key = 'device_token'

    def __init__(self, airship, limit=None):
        params = {'limit': limit} if limit else {}
        super(DeviceTokenList, self).__init__(airship, params)


class ChannelList(DeviceTokenList):
    """Iterator for listing all channels for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`ChannelInfo` object.

    """
    next_url = common.CHANNEL_URL
    data_attribute = 'channels'
    id_key = 'channel_id'


class APIDList(DeviceTokenList):
    """Iterator for listing all APIDs for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    next_url = common.APID_URL
    data_attribute = 'apids'
    id_key = 'apid'


class Feedback(object):
    """Return device tokens or APIDs marked inactive since this timestamp."""

    @classmethod
    def device_token(cls, airship, since):
        url = common.DT_FEEDBACK_URL
        return cls._get_feedback(airship, since, url)

    @classmethod
    def apid(cls, airship, since):
        url = common.APID_FEEDBACK_URL
        return cls._get_feedback(airship, since, url)

    @classmethod
    def _get_feedback(cls, airship, since, url):
        response = airship._request(
            method='GET',
            body='',
            url=url,
            params={'since': since.isoformat()},
            version=3
        )
        data = response.json()
        for r in data:
            try:
                r['marked_inactive_on'] = datetime.datetime.strptime(
                    r['marked_inactive_on'],
                    '%Y-%m-%d %H:%M:%S'
                )
            except:
                r['marked_inactive_on'] = "UNKNOWN"
        return data
