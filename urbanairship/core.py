import logging

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

    def request(self, method, body, url,
                content_type=None, version=None, params=None):
        return self._request(method, body, url,
                             content_type, version, params)

    def _request(self, method, body, url, content_type=None,
                 version=None, params=None, encoding=None):

        headers = \
                {'User-agent': 'UAPythonLib/{0}'.format(__about__.__version__)}
        if content_type:
            headers['Content-type'] = content_type
        if version:
            headers['Accept'] = ('application/vnd.urbanairship+json; '
                                 'version=%d;' % version)
        if encoding:
            headers['Content-Encoding'] = encoding

        logger.debug(
            'Making %s request to %s. Headers:\n\t%s\nBody:\n\t%s',
            method,
            url,
            '\n\t'.join(
                '%s: %s' % (key, value) for (key, value) in headers.items()
            ),
            body
        )

        response = self.session.request(
            method, url, data=body, params=params, headers=headers)

        logger.debug(
            'Received %s response. Headers:\n\t%s\nBody:\n\t%s',
            response.status_code,
            '\n\t'.join(
                '%s: %s' % (key, value) for (key, value)
                in response.headers.items()
            ),
            response.content
        )

        if response.status_code == 401:
            raise common.Unauthorized
        elif not (200 <= response.status_code < 300):
            raise common.AirshipFailure.from_response(response)

        return response

    def create_push(self):
        """Create a Push notification."""
        return Push(self)

    def create_scheduled_push(self):
        """Create a Scheduled Push notification."""
        return ScheduledPush(self)
