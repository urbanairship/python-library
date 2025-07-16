import logging
import re
import warnings
from typing import Any, Dict, Optional

import backoff
import requests

from . import __about__, client, common
from .urls import Urls

logger = logging.getLogger("urbanairship")

VALID_KEY = re.compile(r"^[\w-]{22}$")
VALID_LOCATIONS = ["eu", "us", None]


class Airship(client.BaseClient):
    def __init__(
        self,
        key: str,
        secret: Optional[str] = None,
        token: Optional[str] = None,
        location: str = "us",
        timeout: Optional[int] = None,
        base_url: Optional[str] = None,
        retries: int = 0,
    ):
        """Main client class for interacting with the Airship API.

        :param key: [required] An Airship project key used to authenticate
        :param secret: [optional] The Airship-generated app or master secret for the
        provided key
        :param token: [optional] An Airship-generated bearer token for the provided key
        :param location: [optional] The Airship cloud site your project is associated
        with. Possible values: 'us', 'eu'. Defaults to 'us'.
        :param: timeout: [optional] An integer specifying the number of seconds used
        for a response timeout threshold
        :param base_url: [optional] A string defining an arbitrary base_url to use
        for requests to the Airship API. To be used in place of location.
        :param retries: [optional] An integer specifying the number of times to retry a
        failed request. Retried requests use exponential backoff between requests.
        Defaults to 0, no retry.
        """
        warnings.warn(
            category=DeprecationWarning,
            message="The Airship client class is deprecated. The Airship class has been "
            "aliased to clients.BasicAuthClient. "
            "This class will be removed in version 8.0. If you are importing this "
            "directly, please migrate to clients.BasicAuthClient which should be "
            "a drop-in replacement.",
            stacklevel=2,
        )

        self.key: str = key
        self.secret: Optional[str] = secret
        self.token: Optional[str] = token
        self.location: str = location
        self.timeout: Optional[int] = timeout
        self.retries = retries
        self.urls: Urls = Urls(location=self.location, base_url=base_url)

        if all([secret, token]):
            raise ValueError("One of token or secret must be used, not both")

        self.session = requests.Session()
        if isinstance(token, str):
            self.session.headers.update(
                {"X-UA-Appkey": key, "Authorization": f"Bearer {self.token}"}
            )
        elif isinstance(secret, str):
            self.session.auth = (key, secret)
        else:
            raise ValueError("Either token or secret must be included")

    @property
    def retries(self) -> int:
        return self._retries

    @retries.setter
    def retries(self, value: int):
        self._retries = value

    @property
    def timeout(self) -> Optional[int]:
        return self._timeout

    @timeout.setter
    def timeout(self, value: Optional[int]) -> None:
        if not isinstance(value, int) and value is not None:
            raise ValueError("Timeout must be an integer")
        self._timeout = value

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        if not VALID_KEY.match(value):
            raise ValueError("keys must be 22 characters")
        self._key = value

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        if value not in VALID_LOCATIONS:
            raise ValueError("location must be one of {}".format(VALID_LOCATIONS))
        self._location = value

    @property
    def secret(self) -> Optional[str]:
        return self._secret

    @secret.setter
    def secret(self, value: Optional[str]) -> None:
        if isinstance(value, str) and not VALID_KEY.match(value):
            raise ValueError("secrets must be 22 characters")
        self._secret = value

    @property
    def token(self) -> Optional[str]:
        return self._token

    @token.setter
    def token(self, value: Optional[str]) -> None:
        self._token = value

    def request(
        self,
        method: str,
        body: Any,
        url: str,
        content_type: Optional[str] = None,
        version: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        encoding: Optional[str] = None,
    ) -> requests.Response:
        return self._request(method, body, url, content_type, version, params, encoding)

    def _request(
        self,
        method: str,
        body: Any,
        url: str,
        content_type: Optional[str] = None,
        version: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        encoding: Optional[str] = None,
    ) -> requests.Response:
        headers: Dict[str, str] = {
            "User-agent": "UAPythonLib/{0} {1}".format(__about__.__version__, self.key)
        }
        if content_type:
            headers["Content-type"] = content_type
        if version:
            headers["Accept"] = "application/vnd.urbanairship+json; " "version=%d;" % version
        if encoding:
            headers["Content-Encoding"] = encoding

        @backoff.on_exception(
            backoff.expo,
            (common.AirshipFailure, common.ConnectionFailure),
            max_tries=(self.retries + 1),
        )
        def make_retryable_request(
            method: str,
            url: str,
            body: Any,
            params: Optional[Dict[str, Any]],
            headers: Dict[str, Any],
        ) -> requests.Response:
            try:
                response: requests.Response = self.session.request(
                    method,
                    url,
                    data=body,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                )
            except requests.exceptions.ConnectionError as err:
                raise common.ConnectionFailure(str(err))

            logger.debug(
                "Making %s request to %s. Headers:\n\t%s\nBody:\n\t%s",
                method,
                url,
                "\n\t".join("%s: %s" % (key, value) for (key, value) in headers.items()),
                body,
            )

            logger.debug(
                "Received %s response. Headers:\n\t%s\nBody:\n\t%s",
                response.status_code,
                "\n\t".join("%s: %s" % (key, value) for (key, value) in response.headers.items()),
                response.content,
            )

            if response.status_code == 401:
                raise common.Unauthorized
            elif not (200 <= response.status_code < 300):
                raise common.AirshipFailure.from_response(response)

            result: requests.Response = response
            return result

        return make_retryable_request(method, url, body, params, headers)
