import logging
import json

import six


BASE_URL = 'https://wallet-api.urbanairship.com/v1'

# Template URLs
TEMPLATE_BASE_URL = BASE_URL + '/template/{0}'
TEMPLATE_DUPLICATE_URL = BASE_URL + '/template/duplicate/{0}'
TEMPLATE_ADD_LOCATION_URL = BASE_URL + '/template/{0}/locations/'
TEMPLATE_REMOVE_LOCATION_URL = BASE_URL + '/template/{0}/location/{1}'

# Pass URLs
PASS_BASE_URL = BASE_URL + '/pass/{0}'
PASS_ADD_LOCATION_URL = BASE_URL + '/pass/{0}/locations'
PASS_DELETE_LOCATION_URL = BASE_URL + '/pass/{0}/location/{1}'


logger = logging.getLogger(__name__)


class Unauthorized(Exception):
    """Raised when we get a 401 from the server"""


class ReachFailure(Exception):
    """Raised when we get an error response from the server."""
    def __init__(self, error, error_code, details, response, *args):
        self.error = error
        self.error_code = error_code
        self.details = details
        self.response = response
        super(ReachFailure, self).__init__(*args)

    @classmethod
    def from_response(cls, response):
        """Instantiate a ValidationFailure from a Response object

        Arguments:
            response (response object): Response object used to create a
                failure object.

        Returns:
            A ReachFailure object.
        """
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


class IteratorParent(six.Iterator):
    """An iterator class for listing responses."""
    base_url = None
    data_attribute = None

    def __init__(self, reach, params):
        self.reach = reach
        self.params = params
        self._token_iter = iter(())
        self.page_count = None
        self._page = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._token_iter)
        except StopIteration:
            if self._load_page():
                return next(self._token_iter)
            else:
                raise StopIteration

    def _load_page(self):
        if not self.base_url:
            raise ValueError('base_url cannot be None.')

        response = self.reach.request(
            method='GET',
            body=None,
            url=self.base_url,
            version=1.2,
            params=self.params
        )
        self._page = response.json()
        self.params = self._page.get('pagination')
        if not self.page_count:
            self.page_count = self._page['count']/self.params['pageSize'] + 1
        if self.params['page'] > self.page_count:
            return False
        self.params['page'] += 1
        self._token_iter = iter(self._page[self.data_attribute])
        return True
