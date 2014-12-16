from urbanairship import common

class DeviceInfo(object):
    """Information object for a single device token.

    :ivar id: Device identifier. Also available at the attribute named by the
        ``device_type``.
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

    def next(self):
        try:
            return DeviceInfo.from_payload(self._token_iter.next(), self.id_key)
        except StopIteration:
            self._fetch_next_page()
            return DeviceInfo.from_payload(self._token_iter.next(), self.id_key)

    def _fetch_next_page(self):
        if not self.next_url:
            return
        self._load_page(self.next_url)
        self.next_url = self._page.get('next_page')

    def _load_page(self, url):
        params = {'limit': self.limit} if self.limit is not None else {}
        response = self._airship._request('GET', None, url, version=3, params=params)
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


class APIDList(DeviceList):
    """Iterator for listing all device tokens for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    start_url = common.APID_URL
    data_attribute = 'apids'
    id_key = 'apid'


class DevicePINList(DeviceList):
    """Iterator for listing all device tokens for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`DeviceInfo` object.

    """
    start_url = common.DEVICE_PIN_URL
    data_attribute = 'device_pins'
    id_key = 'device_pin'
