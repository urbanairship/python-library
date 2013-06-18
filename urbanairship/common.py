SERVER = 'go.urbanairship.com'
BASE_URL = "https://go.urbanairship.com/api"
DEVICE_TOKEN_URL = BASE_URL + '/device_tokens/'
APID_URL = BASE_URL + '/apids/'
DEVICE_PIN_URL = BASE_URL + '/device_pins/'
PUSH_URL = BASE_URL + '/push/'
BATCH_PUSH_URL = BASE_URL + '/push/batch/'
BROADCAST_URL = BASE_URL + '/push/broadcast/'
FEEDBACK_URL = BASE_URL + '/device_tokens/feedback/'
RICH_PUSH_SEND_URL = BASE_URL + '/airmail/send/'
RICH_PUSH_BROADCAST_URL = BASE_URL + '/airmail/send/broadcast/'



class Unauthorized(Exception):
    """Raised when we get a 401 from the server"""


class AirshipFailure(Exception):
    """Raised when we get an error response from the server.

    :param status: Status code for the response
    :param message: Response body containting error information.

    """
