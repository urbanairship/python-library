import datetime
from urbanairship import common


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
                payload[key] = datetime.datetime.strptime(
                    payload[key], '%Y-%m-%dT%H:%M:%S'
                )
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


class DeviceInfo(object):
    """Information object for a single device token.

    :ivar id: Device identifier. Also available at the attribute named by
        the ``device_type``.
    :ivar device_type: Type of the device, e.g. ``device_token``
    :ivar active: bool; whether this device can receive notifications.
    :ivar tags: list of tags associated with this device, if any.
    :ivar alias: alias associated with this device, if any.

    """
    id = None
    device_type = None
    active = None
    tags = None
    alias = None

    @classmethod
    def from_payload(cls, payload, device_key):
        """Create based on results from a DeviceList iterator."""
        obj = cls()
        obj.id = payload[device_key]
        obj.device_type = device_key
        for key in payload:
            setattr(obj, key, payload[key])
        return obj


class DevicePINInfo(object):
    @classmethod
    def pin_lookup(cls, airship, device_pin):
        """Retrieve information about this BlackBerry PIN"""
        url = common.DEVICE_PIN_URL + device_pin
        response = airship._request(
            method='GET',
            body=None,
            url=url,
            version=3
        )
        payload = response.json()
        payload['created'] = datetime.datetime.strptime(
            payload['created'], '%Y-%m-%d %H:%M:%S'
        )
        payload['last_registration'] = datetime.datetime.strptime(
            payload['last_registration'], '%Y-%m-%d %H:%M:%S'
        )
        return payload


class DeviceList(object):
    start_url = NotImplemented
    next_url = None
    limit = None
    data_attribute = NotImplemented
    id_key = NotImplemented

    def __init__(self, airship, limit=None):
        self._airship = airship
        self.next_url = self.start_url
        self._token_iter = iter(())
        if limit is not None:
            self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return DeviceInfo.from_payload(next(self._token_iter), self.id_key)
        except StopIteration:
            self._fetch_next_page()
            return DeviceInfo.from_payload(next(self._token_iter), self.id_key)

    def next(self):
        """Necessary for iteration to work with Python 2.*."""
        return self.__next__()

    def _fetch_next_page(self):
        if not self.next_url:
            return
        self._load_page(self.next_url)
        self.next_url = self._page.get('next_page')

    def _load_page(self, url):
        params = {'limit': self.limit} if self.limit is not None else {}
        response = self._airship._request(
            method='GET',
            body=None,
            url=url,
            version=3,
            params=params
        )
        self._page = page = response.json()
        self._token_iter = iter(page[self.data_attribute])


class DeviceTokenList(DeviceList):
    """Iterator for listing all device tokens for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    start_url = common.DEVICE_TOKEN_URL
    data_attribute = 'device_tokens'
    id_key = 'device_token'


class ChannelList(DeviceList):
    """Iterator for listing all channels for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`ChannelInfo` object.

    """
    start_url = common.CHANNEL_URL
    data_attribute = 'channels'
    id_key = 'channel_id'

    def __next__(self):
        try:
            return ChannelInfo.from_payload(
                next(self._token_iter),
                self.id_key
            )
        except StopIteration:
            self._fetch_next_page()
            return ChannelInfo.from_payload(
                next(self._token_iter),
                self.id_key
            )

    def next(self):
        """Necessary for iteration to work with Python 2.*."""
        return self.__next__()


class APIDList(DeviceList):
    """Iterator for listing all APIDs for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    start_url = common.APID_URL
    data_attribute = 'apids'
    id_key = 'apid'


class DevicePINList(DeviceList):
    """Iterator for listing all device PINs for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    start_url = common.DEVICE_PIN_URL
    data_attribute = 'device_pins'
    id_key = 'device_pin'


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
            r['marked_inactive_on'] = datetime.datetime.strptime(
                r['marked_inactive_on'],
                '%Y-%m-%d %H:%M:%S'
            )
        return data
