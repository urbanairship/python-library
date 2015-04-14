import json
import logging


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
