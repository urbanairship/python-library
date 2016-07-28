import logging

SERVER = 'wallet-api.urbanairship.com'
BASE_URL = 'https://wallet-api.urbanairship.com/v1'
TEMPLATE_URL = BASE_URL + '/template/{0}'

# Pass URLs
PASS_BASE_URL = BASE_URL + '/pass/{0}'


logger = logging.getLogger('urbanairship')


class Unauthorized(Exception):
    """Raised when we get a 401 from the server"""


class WalletFailure(Exception):
    """Raised when we get an error response from the server."""
    pass

    @classmethod
    def from_response(cls, response):
        """
        Instantiate a ValidationFailure from a Response object
        :param response: response object used to create failure obj
        """

        raise NotImplementedError
