import json
import logging

from urbanairship import common


logger = logging.getLogger('urbanairship')


class Push(object):
    """A push notification. Set audience, message, etc, and send."""

    def __init__(self, airship):
        self._airship = airship
        self.audience = None
        self.notification = None
        self.device_types = None
        self.options = None
        self.message = None
        self.in_app = None
        self.web_push = None

    @property
    def payload(self):
        data = {
            'audience': self.audience,
            'notification': self.notification,
            'device_types': self.device_types,
        }
        if self.options is not None:
            data['options'] = self.options
        if self.message is not None:
            data['message'] = self.message
        if self.in_app is not None:
            data['in_app'] = self.in_app
        if self.web_push is not None:
            data['web_push'] = self.web_push
        return data

    def send(self):
        """Send the notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """
        body = json.dumps(self.payload)
        response = self._airship._request(
            method='POST',
            body=body,
            url=common.PUSH_URL,
            content_type='application/json',
            version=3
        )

        data = response.json()
        logger.info('Push successful. push_ids: %s',
                    ', '.join(data.get('push_ids', []))
                    )

        return PushResponse(response)


class ScheduledPush(object):
    """A scheduled push notification. Set schedule, push, and send."""

    def __init__(self, airship):
        self._airship = airship
        self.schedule = None
        self.name = None
        self.push = None
        self.url = None

    @classmethod
    def from_url(cls, airship, url):
        """Load an existing scheduled push from its URL."""

        sched = cls(airship)
        response = sched._airship._request(
            method='GET',
            body=None,
            url=url,
            version=3
        )
        payload = response.json()
        sched.name = payload.get('name')
        sched.schedule = payload['schedule']
        sched.push = Push(airship)
        sched.push.audience = payload['push']['audience']
        sched.push.notification = payload['push']['notification']
        sched.push.device_types = payload['push']['device_types']
        if 'message' in payload['push']:
            sched.push.message = payload['push']['message']
        if 'options' in payload['push']:
            sched.push.options = payload['push']['options']
        sched.url = url
        return sched

    @property
    def payload(self):
        data = {
            'schedule': self.schedule,
            'push': self.push.payload,
        }
        if self.name is not None:
            data['name'] = self.name
        return data

    def send(self):
        """Schedule the notification

        :returns: :py:class:`PushResponse` object with ``schedule_url`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """
        body = json.dumps(self.payload)
        response = self._airship._request(
            method='POST',
            body=body,
            url=common.SCHEDULES_URL,
            content_type='application/json',
            version=3
        )

        data = response.json()
        logger.info('Scheduled push successful. schedule_urls: %s',
                    ', '.join(data.get('schedule_urls', [])))
        self.url = data.get('schedule_urls', [None])[0]

        return PushResponse(response)

    def cancel(self):
        """Cancel a previously scheduled notification."""
        if not self.url:
            raise ValueError('Cannot cancel ScheduledPush without url.')
        
        self._airship._request(
            method='DELETE',
            body=None,
            url=self.url,
            version=3
        )

    def update(self):
        if not self.url:
            raise ValueError(
                'Cannot update ScheduledPush without url.')
        body = json.dumps(self.payload)
        response = self._airship._request(
            method='PUT',
            body=body,
            url=self.url,
            content_type='application/json',
            version=3
        )

        data = response.json()
        logger.info('Scheduled push update successful. schedule_urls: %s',
                    ', '.join(data.get('schedule_urls', [])))

        return PushResponse(response)


class PushResponse(object):
    """Response to a successful push notification send or schedule.

    Right now this is a fairly simple wrapper around the json payload response,
    but making it an object gives us some flexibility to add functionality
    later.

    """
    ok = None
    push_ids = None
    schedule_url = None
    operation_id = None
    payload = None

    def __init__(self, response):
        data = response.json()
        self.push_ids = data.get('push_ids')
        self.schedule_url = data.get('schedule_urls', [None])[0]
        self.operation_id = data.get('operation_id')
        self.ok = data.get('ok')
        self.payload = data

    def __str__(self):
        return 'Response Payload: {0}'.format(self.payload)
