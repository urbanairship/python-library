import json
import logging
import warnings

import requests

from . import common, __about__
from .push import Push, ScheduledPush


logger = logging.getLogger('urbanairship')


class AirshipDeviceList(object):
    """Iterator that fetches and returns a list of device tokens

    Follows pagination

    """

    def __init__(self, airship):
        self._airship = airship
        self._load_page(common.DEVICE_TOKEN_URL)

    def __iter__(self):
        return self

    def next(self):
        try:
            return self._token_iter.next()
        except StopIteration:
            self._fetch_next_page()
            return self._token_iter.next()

    def __len__(self):
        return self._page['device_tokens_count']

    def _fetch_next_page(self):
        next_page = self._page.get('next_page')
        if not next_page:
            return
        self._load_page(next_page)

    def _load_page(self, url):
        response = self._airship._request('GET', None, url, version=1)
        self._page = page = response.json()
        self._token_iter = iter(page['device_tokens'])


class Airship(object):

    def __init__(self, key, secret, timeout=None):
        """
        :param timeout: (optional) Float describing the timeout of 
                        the request (in seconds).
        """
        self.key = key
        self.secret = secret
        self.timeout = timeout

        self.session = requests.Session()
        self.session.auth = (key, secret)


    def _request(self, method, body, url, content_type=None,
            version=None, params=None):

        headers = \
                {'User-agent': "UAPythonLib/{0}".format(__about__.__version__)}
        if content_type:
            headers['content-type'] = content_type
        if version is not None:
            headers['Accept'] = \
                "application/vnd.urbanairship+json; version=%d;" % version

        logger.debug("Making %s request to %s. Headers:\n\t%s\nBody:\n\t%s",
            method, url, '\n\t'.join(
                '%s: %s' % (key, value) for (key, value) in headers.items()),
            body)

        response = self.session.request(
            method, url, data=body, params=params, headers=headers,
            timeout=self.timeout)

        logger.debug("Received %s response. Headers:\n\t%s\nBody:\n\t%s",
            response.status_code, '\n\t'.join(
                '%s: %s' % (key, value) for (key, value)
                in response.headers.items()),
            response.content)

        if response.status_code == 401:
            raise common.Unauthorized
        elif not (200 <= response.status_code < 300):
            raise common.AirshipFailure.from_response(response)

        return response

    def register(self, device_token, alias=None, tags=None, badge=None,
            quiettime_start=None, quiettime_end=None, tz=None):
        """Register the device token with UA."""
        url = common.DEVICE_TOKEN_URL + device_token
        payload = {}
        if alias is not None:
            payload['alias'] = alias
        if tags is not None:
            payload['tags'] = tags
        if badge is not None:
            payload['badge'] = badge
        if quiettime_start is not None and quiettime_end is not None:
            payload['quiettime'] = {
                "start": quiettime_start,
                "end": quiettime_end,
            }
        if tz is not None:
            payload['tz'] = tz
        if payload:
            body = json.dumps(payload)
            content_type = 'application/json'
        else:
            body = ''
            content_type = None

        response = self._request('PUT', body, url, content_type,
            version=1)
        return response.status_code == 201

    def deregister(self, device_token):
        """Mark this device token as inactive"""
        url = common.DEVICE_TOKEN_URL + device_token
        self._request('DELETE', '', url, None, version=1)

    def get_device_token_info(self, device_token):
        """Retrieve information about this device token"""
        url = common.DEVICE_TOKEN_URL + device_token
        response = self._request('GET', None, url, version=1)
        return response.json()

    def get_apid_info(self, apid):
        """Retrieve information about this Android APID"""
        url = common.APID_URL + apid
        response = self._request('GET', None, url, version=1)
        return response.json()

    def get_device_pin_info(self, device_pin):
        """Retrieve information about this BlackBerry PIN"""
        url = common.DEVICE_PIN_URL + device_pin
        response = self._request('GET', None, url, version=1)
        return response.json()

    def get_device_tokens(self):
        return AirshipDeviceList(self)

    def push(self, payload, device_tokens=None, aliases=None, tags=None,
            apids=None, device_pins=None, schedules=None):
        """Push this payload to the specified recipients.

        Payload: a dictionary the contents to send, e.g.:
            {'aps': {'alert': 'Hello'}, 'android': {'alert': 'Hello'}}
        device_tokens, apids, aliases, tags, device_pins:
            lists of identifiers to send the notification to
        schedules: list of datetime.datetime objects of when to send this
            notification. If no schedules are present, send immediately.
            Schedules should be in UTC time, not local.

        """
        warnings.warn(
            "Airship.push() is deprecated. See documentation on upgrading.",
            DeprecationWarning)
        if device_tokens:
            payload['device_tokens'] = device_tokens
        if apids:
            payload['apids'] = apids
        if device_pins:
            payload['device_pins'] = device_pins
        if aliases:
            payload['aliases'] = aliases
        if tags:
            payload['tags'] = tags
        if schedules:
            payload['schedule_for'] = [
                schedule.isoformat() for schedule in schedules]
        body = json.dumps(payload)
        self._request('POST', body, common.PUSH_URL,
            'application/json', version=1)

    def batch_push(self, payloads):
        """Push the following payloads as a batch.

        For payload details see:

          http://urbanairship.com/docs/push.html#batch-push

        Summary:
          List of dictionaries, each with:
            * 0 or more "device_tokens", "apids", or "device_pins"
            * 0 or more "aliases" or "tags"
            * "aps" payload, "android" payload, and/or "blackberry".
        """
        warnings.warn(
            "Airship.batch_push() is deprecated. See documentation on upgrading.",
            DeprecationWarning)
        body = json.dumps(payloads)

        self._request('POST', body, common.BATCH_PUSH_URL,
            'application/json', version=1)

    def broadcast(self, payload, exclude_tokens=None, schedules=None):
        """Broadcast this payload to all users."""
        warnings.warn(
            "Airship.broadcast() is deprecated. See documentation on upgrading.",
            DeprecationWarning)
        if exclude_tokens:
            payload['exclude_tokens'] = exclude_tokens
        if schedules:
            payload['schedule_for'] = [
                schedule.isoformat() for schedule in schedules]
        body = json.dumps(payload)
        self._request('POST', body, common.BROADCAST_URL,
            'application/json', version=1)

    def feedback(self, since):
        """Return device tokens marked inactive since this timestamp.

        Returns a list of (device token, timestamp, alias) functions.

        Example:
            airship.feedback(datetime.datetime.utcnow()
                - datetime.timedelta(days=1))

        Note:
            In order to parse the result, we need a sane date parser,
            dateutil: http://labix.org/python-dateutil

        """
        # Make sure that the "since" is not a datetime object.
        try:
            since = since.date()
        except AttributeError:
            pass
        url = common.FEEDBACK_URL
        response = self._request('GET', '', url,
            params={'since': since.isoformat()}, version=1)
        data = response.json()
        try:
            from dateutil.parser import parse
        except ImportError:
            def parse(x):
                return x
        return [
            (r['device_token'], parse(r['marked_inactive_on']), r['alias'])
            for r in data]

    def create_push(self):
        """Create a Push notification."""
        return Push(self)

    def create_scheduled_push(self):
        """Create a Scheduled Push notification."""
        return ScheduledPush(self)

    def create_rich_push(self):
        """Create a RichPush message."""
        warnings.warn(
            "Airship.create_rich_push() is deprecated. See documentation on upgrading.",
            DeprecationWarning)
        return RichPush(self)


class RichPush(object):
    """A Rich Push message. Set recipients, message, and options, then send."""

    def __init__(self, airship):
        self._airship = airship
        self.users = []
        self.aliases = []
        self.tags = []
        self.title = None
        self.message = None
        self.content_type = None
        self.push = None
        self.extra = None

    def add_recipients(self, users=None, aliases=None, tags=None):
        """Add one or more user IDs, aliases, or tags."""

        if users is not None:
            self.users = users
        if aliases is not None:
            self.aliases = aliases
        if tags is not None:
            self.tags = tags

    def set_message(self, title, message, content_type='text/html'):
        """Set the Rich Push title and message body."""

        self.title = title
        self.message = message
        self.content_type = content_type
        if self.push is None:
            self.push = {"aps": {"alert": title}}

    def set_push(self, push):
        """Specify the push notification payload to be delivered.

        Default is to send an alert to iOS devices with the specified title.
        """

        self.push = push

    def set_extra(self, **kw):
        """Set extra key and values for the rich push message."""

        self.extra = kw

    def send(self):
        """Send the rich push message."""

        if not self.users and not self.aliases and not self.tags:
            raise ValueError("No recipients specified")
        payload = {
            "title": self.title,
            "message": self.message,
            "content-type": self.content_type,
        }
        if self.push:
            payload['push'] = self.push
        if self.users:
            payload['users'] = self.users
        if self.aliases:
            payload['aliases'] = self.aliases
        if self.tags:
            payload['tags'] = self.tags
        if self.extra:
            payload['extra'] = self.extra
        body = json.dumps(payload)
        self._airship._request('POST', body,
            common.RICH_PUSH_SEND_URL, 'application/json', version=1)

    def broadcast(self):
        """Broadcast the rich push message to all users."""

        if self.users or self.aliases or self.tags:
            raise ValueError("Recipients cannot be specified for a broadcast")
        payload = {
            "title": self.title,
            "message": self.message,
            "content-type": self.content_type,
        }
        if self.push:
            payload['push'] = self.push
        if self.extra:
            payload['extra'] = self.extra
        body = json.dumps(payload)
        self._airship._request('POST', body,
            common.RICH_PUSH_BROADCAST_URL, 'application/json', version=1)

