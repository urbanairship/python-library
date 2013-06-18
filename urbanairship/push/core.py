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
        self.message = None

    def send(self):
        """Send the notification.

        :returns: Dictionary with response information, including ``push_id``.
        :raises AirshipFailure: Request failed. See args for status and
            response body.
        :raises Unauthorized: Authentication failed.

        """
        payload = {
            "audience": self.audience,
            "notification": self.notification,
            "device_types": self.device_types,
        }
        if self.options is not None:
            payload['options'] = self.options
        if self.message is not None:
            payload['message'] = self.message

        body = json.dumps(payload)
        status, response = self._airship._request('POST', body,
            common.PUSH_URL, 'application/json', 3)
        if status < 200 or status >= 300:
            raise common.AirshipFailure(status, response)

        return json.loads(response)
