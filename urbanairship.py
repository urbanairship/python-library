"""Python module for using the Urban Airship API"""

import httplib
import urllib
try:
    import json
except ImportError:
    import simplejson as json


SERVER = 'go.urbanairship.com'
BASE_URL = "https://go.urbanairship.com/api"
DEVICE_TOKEN_URL = BASE_URL + '/device_tokens/'
PUSH_URL = BASE_URL + '/push/'
BROADCAST_URL = BASE_URL + '/push/broadcast/'
FEEDBACK_URL = BASE_URL + '/device_tokens/feedback/'


class Unauthorized(Exception):
    """Raised when we get a 401 from the server"""


class AirshipFailure(Exception):
    """Raised when we get an error response from the server.

    args are (status code, message)

    """


class Airship(object):

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

        self.auth_string = ('%s:%s' % (key, secret)).encode('base64')[:-1]

    def _request(self, method, body, url, content_type=None):
        h = httplib.HTTPSConnection(SERVER)
        headers = {
            'authorization': 'Basic %s' % self.auth_string,
        }
        if content_type:
            headers['content-type'] = content_type
        h.request(method, url, body=body, headers=headers)
        resp = h.getresponse()
        if resp.status == 401:
            raise Unauthorized

        return resp.status, resp.read()

    def register(self, device_token, alias=None, tags=None):
        """Register the device token with UA."""
        url = DEVICE_TOKEN_URL + device_token
        if alias is not None or tags is not None:
            payload = {'alias': alias}
            if tags:
                payload['tags']= tags
            body = json.dumps(payload)
            content_type = 'application/json'
        else:
            body = ''
            content_type = None

        status, response = self._request('PUT', body, url, content_type)
        if not status in (200, 201):
            raise AirshipFailure(status, response)

    def push(self, payload, device_tokens=None, aliases=None, tags=None):
        """Push this payload to the specified device tokens and tags."""
        if device_tokens:
            payload['device_tokens'] = device_tokens
        if aliases:
            payload['aliases'] = aliases
        if tags:
            payload['tags'] = tags
        body = json.dumps(payload)
        status, response = self._request('POST', body, PUSH_URL,
            'application/json')
        if not status == 200:
            raise AirshipFailure(status, response)

    def broadcast(self, payload, exclude_tokens=None):
        """Broadcast this payload to all users."""
        if exclude_tokens:
            payload['exclude_tokens'] = exclude_tokens
        body = json.dumps(payload)
        status, response = self._request('POST', body, PUSH_URL,
            'application/json')
        if not status == 200:
            raise AirshipFailure(status, response)

    def feedback(self, since):
        """Return device tokens marked inactive since this timestamp.

        Returns a list of (device token, timestamp, alias) functions.

        Example:
            airship.feedback(datetime.datetime.utcnow()
                - datetime.interval(days=1))

        Note:
            In order to parse the result, we need a sane date parser,
            dateutil: http://labix.org/python-dateutil

        """
        url = FEEDBACK_URL + '?' + \
            urllib.urlencode({'since': since.isoformat()})
        status, response = self._request('GET', '', url)
        if not status == 200:
            raise AirshipFailure(status, response)
        data = json.loads(response)
        try:
            from dateutil.parser import parse
        except ImportError:
            def parse(x):
                return x
        return [
            (r['device_token'], parse(r['marked_inactive_on']), r['alias'])
            for r in data]
