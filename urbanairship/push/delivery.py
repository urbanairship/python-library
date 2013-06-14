import json

from urbanairship import common


class Push(object):
    """A push notification. Set audience, message, etc, and send."""

    def __init__(self, airship):
        self._airship = airship
        self.audience = None
        self.notification = None
        self.device_types = None
        self.options = None

    def validate(self):
        """Confirm the notification is valid.

        Automatically called by send, but can be called directly.
        """
        raise NotImplementedError

    def send(self):
        """Send the notification."""

        payload = {
            "audience": self.audience,
            "notification": self.notification,
            "device_types": self.device_types,
        }
        if self.options is not None:
            payload['options'] = self.options

        body = json.dumps(payload)
        status, response = self._airship._request('POST', body,
            common.PUSH_URL, 'application/json', 3)
        if status < 200 or status >= 300:
            raise common.AirshipFailure(status, response)
