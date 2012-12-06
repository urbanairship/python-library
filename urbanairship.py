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
BATCH_PUSH_URL = BASE_URL + '/push/batch/'
BROADCAST_URL = BASE_URL + '/push/broadcast/'
FEEDBACK_URL = BASE_URL + '/device_tokens/feedback/'
# Try to import the requests library http://pypi.python.org/pypi/requests 
# fall back to httplib if not available.
REQUESTS_AVAILABLE = False
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    import httplib
# utility function to fallback to httplib
def http_request(method, url, **kwargs):
    if REQUESTS_AVAILABLE:
        try:
            # convert body argument to requests supported argument
            if kwargs.has_key('body'):
                kwargs['data'] = kwargs['body']
                del kwargs['body']

            resp = requests.request(method, url, **kwargs)
            resp.status = resp.status_code
            return resp
        except requests.exceptions.RequestException, e:
            raise AirshipFailure(None, str(e))
    else:
        h = httplib.HTTPSConnection(SERVER)
        h.request(method, url, **kwargs)
        resp = h.getresponse()
        resp.content = resp.read()
        return resp

class Unauthorized(Exception):
    """Raised when we get a 401 from the server"""


class AirshipFailure(Exception):
    """Raised when we get an error response from the server.

    args are (status code, message)

    """


class AirshipDeviceList(object):
    """Iterator that fetches and returns a list of device tokens

    Follows pagination

    """

    def __init__(self, airship):
        self._airship = airship
        self._load_page(DEVICE_TOKEN_URL)

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
        status, response = self._airship._request('GET', None, url)
        if status != 200:
            raise AirshipFailure(status, response)
        self._page = page = json.loads(response)
        self._token_iter = iter(page['device_tokens'])


class Airship(object):

    def __init__(self, key, secret, timeout=None):
        self.key = key
        self.secret = secret
        self.timeout = 240 # default 4 minutes
        if timeout is not None:
            self.timeout = timeout
        self.auth_string = ('%s:%s' % (key, secret)).encode('base64')[:-1]

    def _request(self, method, body, url, content_type=None):
        headers = {
            'authorization': 'Basic %s' % self.auth_string,
        }
        if content_type:
            headers['content-type'] = content_type
        resp = http_request(method,url,body=body,headers=headers,timeout=self.timeout)
        if resp.status == 401:
            raise Unauthorized

        return resp.status, resp.content

    def register(self, device_token, alias=None, tags=None, badge=None):
        """Register the device token with UA."""
        url = DEVICE_TOKEN_URL + device_token
        payload = {}
        if alias is not None:
            payload['alias'] = alias
        if tags is not None:
            payload['tags'] = tags
        if badge is not None:
            payload['badge'] = badge
        if payload:
            body = json.dumps(payload)
            content_type = 'application/json'
        else:
            body = ''
            content_type = None

        status, response = self._request('PUT', body, url, content_type)
        if not status in (200, 201):
            raise AirshipFailure(status, response)
        return status == 201

    def deregister(self, device_token):
        """Mark this device token as inactive"""
        url = DEVICE_TOKEN_URL + device_token
        status, response = self._request('DELETE', '', url, None)
        if status != 204:
            raise AirshipFailure(status, response)

    def get_device_token_info(self, device_token):
        """Retrieve information about this device token"""
        url = DEVICE_TOKEN_URL + device_token
        status, response = self._request('GET', None, url)
        if status == 404:
            return None
        elif status != 200:
            raise AirshipFailure(status, response)
        return json.loads(response)

    def get_device_tokens(self):
        return AirshipDeviceList(self)

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

    def batch_push(self, payloads):
        """Push the following payloads as a batch.

        For payload details see:

          http://urbanairship.com/docs/push.html#batch-push

        Summary:
          List of dictionaries, each with:
            * 0 or more "device_tokens"
            * 0 or more "aliases"
            * "aps" payload.
        """
        body = json.dumps(payloads)

        status, response = self._request('POST', body, BATCH_PUSH_URL,
            'application/json')
        if not status == 200:
            raise AirshipFailure(status, response)

    def broadcast(self, payload, exclude_tokens=None):
        """Broadcast this payload to all users."""
        if exclude_tokens:
            payload['exclude_tokens'] = exclude_tokens
        body = json.dumps(payload)
        status, response = self._request('POST', body, BROADCAST_URL,
            'application/json')
        if not status == 200:
            raise AirshipFailure(status, response)

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
