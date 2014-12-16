import json
import logging
import warnings

import requests

from . import common, __about__
from .push import Push, ScheduledPush


logger = logging.getLogger('urbanairship')


class Airship(object):

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

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
            method, url, data=body, params=params, headers=headers)

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

    def get_device_pin_info(self, device_pin):
        """Retrieve information about this BlackBerry PIN"""
        url = common.DEVICE_PIN_URL + device_pin
        response = self._request('GET', None, url, version=1)
        return response.json()

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