import json
import logging
import datetime

SERVER = 'go.urbanairship.com'
BASE_URL = "https://go.urbanairship.com/api"
CHANNEL_URL = BASE_URL + '/channels/'
DEVICE_TOKEN_URL = BASE_URL + '/device_tokens/'
APID_URL = BASE_URL + '/apids/'
DEVICE_PIN_URL = BASE_URL + '/device_pins/'
PUSH_URL = BASE_URL + '/push/'
DT_FEEDBACK_URL = BASE_URL + '/device_tokens/feedback/'
APID_FEEDBACK_URL = BASE_URL + '/apids/feedback/'
SCHEDULES_URL = BASE_URL + '/schedules/'
TAGS_URL = BASE_URL + '/tags/'
SEGMENTS_URL = BASE_URL + '/segments/'
REPORTS_URL = BASE_URL + '/reports/'
LISTS_URL = BASE_URL + '/lists/'

NAMED_USER_URL = BASE_URL + '/named_users/'
NAMED_USER_TAG_URL = NAMED_USER_URL + 'tags/'
NAMED_USER_DISASSOCIATE_URL = NAMED_USER_URL + 'disassociate/'
NAMED_USER_ASSOCIATE_URL = NAMED_USER_URL + 'associate/'

logger = logging.getLogger('urbanairship')


class Unauthorized(Exception):
    """Raised when we get a 401 from the server"""


class AirshipFailure(Exception):
    """Raised when we get an error response from the server.


    :param args: For backwards compatibility, ``*args`` includes the status and
        response body.

    """

    error = None
    error_code = None
    details = None
    response = None

    def __init__(self, error, error_code, details, response, *args):
        self.error = error
        self.error_code = error_code
        self.details = details
        self.response = response
        super(AirshipFailure, self).__init__(*args)

    @classmethod
    def from_response(cls, response):
        """Instantiate a ValidationFailure from a Response object"""

        try:
            payload = response.json()
            error = payload.get('error')
            error_code = payload.get('error_code')
            details = payload.get('details')
        except ValueError:
            error = response.reason
            error_code = None
            details = response.content

        logger.error(
            "Request failed with status %d: '%s %s': %s",
            response.status_code, error_code, error, json.dumps(details))

        return cls(
            error,
            error_code,
            details,
            response,
            response.status_code,
            response.content
        )


class IteratorParent(object):
    next_url = None
    data_attribute = None
    data_list = None
    params = None

    def __init__(self, airship, params):
        self.airship = airship
        self.params = params
        self._token_iter = iter(())

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return IteratorDataObj.from_payload(next(self._token_iter))
        except StopIteration:
            if self._load_page():
                return IteratorDataObj.from_payload(next(self._token_iter))
            else:
                raise StopIteration

    def next(self):
        """Necessary for iteration to work with Python 2.*."""
        return self.__next__()

    def _load_page(self):
        if not self.next_url:
            return False
        response = self.airship.request(
            method='GET',
            body=None,
            url=self.next_url,
            version=3,
            params=self.params
        )
        self.params = None
        self._page = response.json()
        check_url = self._page.get('next_page')
        if check_url == self.next_url:
            return False
        self.next_url = check_url
        self._token_iter = iter(self._page[self.data_attribute])
        return True


class IteratorDataObj(object):
    @classmethod
    def from_payload(cls, payload):
        obj = cls()
        for key in payload:
            try:
                val = datetime.datetime.strptime(payload[key], '%Y-%m-%d %H:%M:%S')
            except (TypeError, ValueError):
                val = payload[key]
            setattr(obj, key, val)
        return obj

    def __str__(self):
        print_str = ""
        for attr in dir(self):
            if not attr.startswith('__') and attr != 'from_payload':
                print_str += attr + ': ' + str(getattr(self, attr)) + ', '
        return print_str[:-2]
