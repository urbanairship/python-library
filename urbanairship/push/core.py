import json
import logging
import warnings

from urbanairship import devices


logger = logging.getLogger('urbanairship')


class Push(object):
    """A push notification. Set audience, message, etc, and send."""

    def __init__(self, airship):
        self._airship = airship
        self.audience = None
        self.notification = None
        self._device_types = None
        self.options = None
        self.campaigns = None
        self.message = None
        self.in_app = None

    @property
    def payload(self):
        data = {
            'audience': self.audience,
            'notification': self.notification,
            'device_types': self.device_types,
        }
        if self.options is not None:
            data['options'] = self.options
        if self.campaigns is not None:
            data['campaigns'] = self.campaigns
        if self.message is not None:
            data['message'] = self.message
        if self.in_app is not None:
            data['in_app'] = self.in_app
        return data

    @property
    def device_types(self):
        return self._device_types

    @device_types.setter
    def device_types(self, types):
        if types == 'all' or (len(types) == 1 and types[0] == 'all'):
            warnings.warn(
                "The device type 'all' has been deprecated.",
                DeprecationWarning
            )
        self._device_types = types

    def send(self):
        """Send the notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.
        :raises ValueError: Required keys missing or incorrect values included.
        """
        if 'email' in self.payload['notification']:
            if self.payload['device_types'] == 'all':
                raise ValueError(
                    'device_types cannot be all when including an email override'
                )
            if 'email' not in self.payload['device_types']:
                raise ValueError(
                    'email must be in device_types if email override is included'
                )
        if 'email' in self.payload['device_types'] \
                and 'email' not in self.payload['notification']:
            raise ValueError(
                'email override must be included when email is in device_types'
            )

        body = json.dumps(self.payload)
        response = self._airship._request(
            method='POST',
            body=body,
            url=self._airship.urls.get('push_url'),
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

    @classmethod
    def from_payload(cls, payload, id_key, airship):
        """Create based on results from a ScheduledList iterator."""
        obj = cls(airship)
        obj._schedule_id = payload[id_key]
        for key in payload:
            setattr(obj, key, payload[key])
        return obj

    @property
    def payload(self):
        if hasattr(self.push, 'merge_data'):  # create template payload
            data = self.push.payload
            data['schedule'] = self.schedule
        elif isinstance(self.push, CreateAndSendPush):  # create cas payload
            if 'scheduled_time' not in self.schedule:
                raise ValueError(
                    'only scheduled_time supported with create and send schedules'
                )
            data = {
                'schedule': self.schedule,
                'push': self.push.payload
            }
        else:
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

        if hasattr(self.push, 'merge_data'):
            url = self._airship.urls.get('schedule_template_url')
        elif isinstance(self.push, CreateAndSendPush):
            url = self._airship.urls.get('schedule_create_and_send_url')
        else:
            url = self._airship.urls.get('schedules_url')

        response = self._airship._request(
            method='POST',
            body=body,
            url=url,
            content_type='application/json',
            version=3
        )
        data = response.json()

        urls = data.get('schedule_urls', [])
        if urls:
            self.url = urls[0]
            logger.info('Scheduled push successful. schedule_urls: %s',
                        ', '.join(data.get('schedule_urls', [])))

        else:
            logger.info('Scheduled push resulted in zero messages scheduled.')

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


class TemplatePush(object):
    """A personalized push notification. Set details and send."""

    def __init__(self, airship):
        self._airship = airship
        self.audience = None
        self.device_types = None
        self.merge_data = None

    @property
    def payload(self):
        data = {
            'audience': self.audience,
            'device_types': self.device_types,
            'merge_data': self.merge_data
        }

        return data

    def send(self):
        """Send the personalized notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """

        if not self.audience:
            raise ValueError('Must set audience for template push.')

        if not self.device_types:
            raise ValueError('Must set device_types for template push.')

        body = json.dumps(self.payload)
        response = self._airship._request(
            method='POST',
            body=body,
            url=self._airship.urls.get('templates_url') + 'push',
            content_type='application/json',
            version=3
        )

        data = response.json()
        logger.info('Push successful. push_ids: %s',
                    ', '.join(data.get('push_ids', []))
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

    def __init__(self, airship, channels=[]):
        self._airship = airship
        self.channels = channels
        self.notification = None
        self.campaigns = None

    @property
    def device_types(self):
        return self._device_types

    @device_types.setter
    def device_types(self, values):
        accepted_device_types = ('sms', 'email', 'open::')

        if len(values) != 1:
            raise ValueError('only a single device_type may be used.')

        for value in values:
            if value[:6] not in accepted_device_types:
                raise ValueError(
                    'device_types must be one of {}'.format(
                        str(accepted_device_types)
                        )
                    )

        self._device_types = values

    @property
    def audience(self):
        if 'email' in self.device_types:
            return self._email_audience()
        elif 'sms' in self.device_types:
            return self._sms_audience()
        else:
            return self._open_channel_audience()

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, value):
        if type(value) is not list:
            raise TypeError('channels must be a list')
        if len(value) > 1000:
            raise ValueError('channels list must have 1000 or fewer items')

        self._channels = value

    @property
    def payload(self):
        data = {
            'audience': self.audience,
            'notification': self.notification,
            'device_types': self.device_types
        }
        if self.campaigns is not None:
            data['campaigns'] = self.campaigns
        return data

    def _email_audience(self):
        addresses = []
        for email in self.channels:
            if not isinstance(email, devices.Email):
                raise TypeError(
                    'Can only use email channels when device_types is email'
                )
            addresses.append(email.create_and_send_audience)
        audience = {'create_and_send': addresses}

        return audience

    def _sms_audience(self):
        addresses = []
        for sms in self.channels:
            if not isinstance(sms, devices.Sms):
                raise TypeError(
                    'Can only use Sms objects when device_types is sms'
                    )
            addresses.append(sms.create_and_send_audience)
        audience = {'create_and_send': addresses}

        return audience

    def _open_channel_audience(self):
        addresses = []
        for open_channel in self.channels:
            if not isinstance(open_channel, devices.OpenChannel):
                raise TypeError(
                    'Can only use OpenChannel objects when device_types is open::'
                )
            addresses.append(open_channel.create_and_send_audience)
        audience = {'create_and_send': addresses}

        return audience

    def send(self):
        """Send the notification.

        :returns: :py:class:`PushResponse` object with ``push_ids`` and
            other response data.
        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.
        :raises ValueError: Required keys missing or incorrect values included.
        """
        body = json.dumps(self.payload)
        response = self._airship._request(
            method='POST',
            body=body,
            url=self._airship.urls.get('create_and_send_url'),
            content_type='application/json',
            version=3
        )

        logger.info('Create and Send successful')

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
        self.schedule_url = data.get('schedule_urls', [])
        self.operation_id = data.get('operation_id')
        self.ok = data.get('ok')
        self.payload = data

    def __str__(self):
        return 'Response Payload: {0}'.format(self.payload)
