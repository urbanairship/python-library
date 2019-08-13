import logging
import datetime
import six


class Urls(object):
    def __init__(self, location=None):
        if not location or location == 'us':
            self.base_url = 'https://go.urbanairship.com/api/'
        elif location == 'eu':
            self.base_url = 'https://go.airship.eu/api/'

        self.channel_url = self.base_url + 'channels/'
        self.open_channel_url = self.channel_url + 'open/'
        self.device_token_url = self.base_url + 'device_tokens/'
        self.apid_url = self.base_url + 'apids/'
        self.push_url = self.base_url + 'push/'
        self.schedules_url = self.base_url + 'schedules/'
        self.tags_url = self.base_url + 'tags/'
        self.segments_url = self.base_url + 'segments/'
        self.reports_url = self.base_url + 'reports/'
        self.lists_url = self.base_url + 'lists/'
        self.location_url = self.base_url + 'location/'

        self.templates_url = self.base_url + 'templates/'
        self.schedule_template_url = self.templates_url + 'schedules/'

        self.pipelines_url = self.base_url + 'pipelines/'

        self.named_user_url = self.base_url + 'named_users/'
        self.named_user_tag_url = self.named_user_url + 'tags/'
        self.named_user_disassociate_url = self.named_user_url + 'disassociate/'
        self.named_user_associate_url = self.named_user_url + 'associate/'

        self.sms_url = self.channel_url + 'sms/'
        self.sms_opt_out_url = self.sms_url + 'opt-out/'
        self.sms_uninstall_url = self.sms_url + 'uninstall/'

        self.email_url = self.channels_url + 'email/'
        self.email_tags_url = self.email_url + 'tags/'
        self.email_uninstall_url = self.email_url + 'uninstall/'

        self.create_and_send_url = self.base_url + 'create-and-send/'
        self.schedule_create_and_send_url = self.schedules_url + 'create-and-send/'

    def get(self, endpoint):
        url = getattr(self, endpoint, None)

        if not url:
            raise AttributeError('No url for endpoint %s' % endpoint)

        return url

EXPERIMENTS_URL = BASE_URL + '/experiments'
EXPERIMENTS_SCHEDULE_URL = EXPERIMENTS_URL + '/scheduled'
EXPERIMENTS_VALIDATE = EXPERIMENTS_URL + '/validate'

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
        """
        Instantiate a ValidationFailure from a Response object
        :param response: response object used to create failure obj
        """
        try:
            payload = response.json()
            error = payload.get('error')
            error_code = payload.get('error_code')
            details = payload.get('details')
        except (ValueError, TypeError, KeyError):
            error = response.reason
            error_code = response.status_code
            details = response.content

        logger.error(
            "Request failed with status %d: '%s %s': %s",
            response.status_code, error_code, error, details)

        return cls(
            error,
            error_code,
            details,
            response,
            response.status_code,
            response.content
        )


@six.python_2_unicode_compatible
class IteratorDataObj(object):
    @classmethod
    def from_payload(cls, payload, device_key=None, airship=None):
        obj = cls()
        if device_key:
            obj.device_type = device_key
        if device_key and payload[device_key]:
            obj.id = payload[device_key]
        if airship:
            obj.airship = airship
        for key in payload:
            try:
                val = datetime.datetime.strptime(
                    payload[key],
                    '%Y-%m-%d %H:%M:%S'
                )
            except (TypeError, ValueError):
                val = payload[key]
            setattr(obj, key, val)
        return obj

    def __str__(self):
        print_str = ""
        for attr in dir(self):
            if(
                not attr.startswith('__') and
                not hasattr(getattr(self, attr), '__call__')
            ):
                print_str += attr + ': ' + str(getattr(self, attr)) + ', '
        return print_str[:-2]


class IteratorParent(six.Iterator):
    next_url = None
    data_attribute = None
    data_list = None
    params = None
    id_key = None
    instance_class = IteratorDataObj

    def __init__(self, airship, params):
        self.airship = airship
        self.params = params
        self._token_iter = iter(())

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.instance_class.from_payload(
                next(self._token_iter),
                self.id_key,
                self.airship
            )
        except StopIteration:
            if self._load_page():
                return self.instance_class.from_payload(
                    next(self._token_iter),
                    self.id_key,
                    self.airship
                )
            else:
                raise StopIteration

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
