"""Python module for using the Urban Airship API"""

import httplib
import urllib
try:
    import simplejson as json
except ImportError:
    import json


SERVER = 'go.urbanairship.com'
BASE_URL = "https://go.urbanairship.com/api"
DEVICE_TOKEN_URL = BASE_URL + '/device_tokens/'
APIDS_TOKEN_URL = BASE_URL + '/apids/'
PUSH_URL = BASE_URL + '/push/'
BATCH_PUSH_URL = BASE_URL + '/push/batch/'
BROADCAST_URL = BASE_URL + '/push/broadcast/'
FEEDBACK_URL = BASE_URL + '/device_tokens/feedback/'


class Unauthorized(Exception):
    """Raised when we get a 401 from the server"""


class AirshipFailure(Exception):
    """Raised when we get an error response from the server.
    args are (status code, message)
    """


class AirshipList(object):
    """Parent class that represents a list of iOS devices or
    Android C2DM APIDs. Only meant to be used by subclasses.
    """
    def __init__(self, airship):
      self._airship = airship


class AirshipDeviceList(AirshipList):
    """Iterator that fetches and returns a list of iOS device tokens
    Follows pagination.
    """
    def __init__(self, airship):
        super(AirshipDeviceList, self).__init__(airship)
        self._load_page(DEVICE_TOKEN_URL)

    def __len__(self):
        return self._page['device_tokens_count']

    def _load_page(self, url):
        status, response = self._airship._request('GET', None, url)
        if status != 200:
            raise AirshipFailure(status, response)
        self._page = page = json.loads(response)
        self._token_iter = iter(page['device_tokens'])


class AirshipAPIDsList(AirshipList):
    """Iterator that fetches and returns a list of Android
    C2DM APIDs.
    """
    def __init__(self, airship):
        super(AirshipAPIDsList, self).__init__(airship)
        self._load_page(APIDS_TOKEN_URL)

    def __len__(self):
        return len(self._page['apids'])

    def _load_page(self, url):
        status, response = self._airship._request('GET', None, url)
        if status != 200:
            raise AirshipFailure(status, response)
        self._page = page = json.loads(response)
        self._token_iter = iter(page['apids'])


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
            import pdb; pdb.set_trace()
            raise Unauthorized
        return resp.status, resp.read()

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

    def registerAPID(self, APID_token, c2dm_registration_id, alias=None, \
        tags=None, badge=None):
        """Register APID token with UA."""
        url = APIDS_TOKEN_URL + APID_token
        payload = {}
        if alias is not None:
            payload['alias'] = alias
        if tags is not None:
            payload['tags'] = tags
        if badge is not None:
            payload['badge'] = badge
        if c2dm_registration_id:
            payload['c2dm_registration_id'] = c2dm_registration_id
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


    def deregister(self, device_token, url=None):
        """Mark this device token as inactive"""
        if url == None:
          url = DEVICE_TOKEN_URL + device_token
        status, response = self._request('DELETE', '', url, None)
        if status != 204:
            raise AirshipFailure(status, response)

    def deregisterAPID(self, APID_token):
        """Mark this APID token as inactive."""
        url = APIDS_TOKEN_URL + APID_token
        self.deregister(APID_token, url)

    def get_device_token_info(self, device_token, url=None):
        """Retrieve information about this device token"""
        if url == None:
          url = DEVICE_TOKEN_URL + device_token
        status, response = self._request('GET', None, url)
        if status == 404:
            return None
        elif status != 200:
            raise AirshipFailure(status, response)
        return json.loads(response)

    def get_APID_token_info(self, APID_token):
        """Retrieve information about this APID token"""
        url = APIDS_TOKEN_URL + APID_token
        return self.get_device_token_info(APID_token, url)

    def get_device_tokens(self):
        return AirshipDeviceList(self)

    def get_apids(self):
        return AirshipAPIDsList(self)

    def push(self, payload, device_tokens=None, aliases=None, tags=None, schedule_for=None, APID_tokens=None):
        """Push this payload to the specified device tokens and tags."""
        if device_tokens:
            payload['device_tokens'] = device_tokens
        if APID_tokens:
            payload['apids'] = APID_tokens
        if aliases:
            payload['aliases'] = aliases
        if tags:
            payload['tags'] = tags
        if schedule_for:
            payload['schedule_for'] = schedule_for
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

