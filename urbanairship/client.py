import logging
import re
import time
import uuid
from typing import Any, Dict, List, Optional

import backoff
import jwt
import requests
from requests.exceptions import ConnectionError, Timeout

from urbanairship.urls import Urls

from . import __about__, common

logger = logging.getLogger("urbanairship")

VALID_KEY = re.compile(r"^[\w-]{22}$")
VALID_LOCATIONS = ["eu", "us", None]
DEFAULT_REQ_TIMEOUT_S = 60
DEFAULT_API_VERSION = 3
DEFAULT_ASSERTION_EXPIRY = 61
US_OAUTH_URL = "https://oauth2.asnapius.com"
EU_OAUTH_URL = "https://oauth2.asnapieu.com"


class BaseClient:
    """Base client class for interacting with the Airship API

    :param key: [required] An airship app key (project key) which identifies the project
    :param location: [optional] The Airship cloud site the project is located in.
        May be 'us' or 'eu'. Defaults to 'us'.
    :param timeout: [optional]  An integer specifying the number of seconds used
        for a response timeout threshold
    :param base_url: [optional] A string defining an arbitrary base_url to use
        for requests to the Airship API. To be used in place of location.
    :param retries: [optional] An integer specifying the number of times to retry a
        failed request. Retried requests use exponential backoff between requests.
        Defaults to 0, no retry.
    """

    def __init__(
        self,
        key: str,
        location: str = "us",
        timeout: int = DEFAULT_REQ_TIMEOUT_S,
        retries: int = 0,
        base_url: Optional[str] = None,
    ) -> None:
        self.key = key
        self.location = location
        self.timeout = timeout
        self.retries = retries
        self.base_url = base_url
        self.urls: Urls = Urls(location=self.location, base_url=self.base_url)
        self.session = requests.Session()

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
        """location of the cloud site project belongs to. 'us' or 'eu'"""
        return self._location

    @location.setter
    def location(self, value: str):
        if value not in VALID_LOCATIONS:
            raise ValueError(f"location must be one of {format(VALID_LOCATIONS)}")
        self._location = value

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

    def request(
        self,
        method: str,
        body: Any,
        url: str,
        content_type: Optional[str] = None,
        version: int = DEFAULT_API_VERSION,
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
        version: int = DEFAULT_API_VERSION,
        params: Optional[Dict[str, Any]] = None,
        encoding: Optional[str] = None,
    ) -> requests.Response:
        headers: Dict[str, str] = {
            "User-agent": "UAPythonLib/{0} {1}".format(__about__.__version__, self.key)
        }
        if content_type:
            headers["Content-type"] = content_type
        if version:
            headers["Accept"] = (
                "application/vnd.urbanairship+json; " f"version={version};"
            )
        if encoding:
            headers["Content-Encoding"] = encoding
        self.session.headers.update(headers)

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
            self.session.headers.update(headers)
            logger.debug(
                "Making %s request to %s. Headers:\n\t%s\nBody:\n\t%s",
                method,
                url,
                "\n\t".join(
                    "%s: %s" % (key, value) for (key, value) in headers.items()
                ),
                body,
            )
            try:
                response: requests.Response = self.session.request(
                    method,
                    url,
                    data=body,
                    params=params,
                    timeout=self.timeout,
                )
            except requests.exceptions.ConnectionError as err:
                raise common.ConnectionFailure(str(err))

            logger.debug(
                "Received %s response. Headers:\n\t%s\nBody:\n\t%s",
                response.status_code,
                "\n\t".join(
                    "%s: %s" % (key, value) for (key, value) in response.headers.items()
                ),
                response.content,
            )

            if response.status_code == 401:
                raise common.Unauthorized
            elif not (200 <= response.status_code < 300):
                raise common.AirshipFailure.from_response(response)

            return response

        return make_retryable_request(method, url, body, params, headers)


class BasicAuthClient(BaseClient):
    """
    Client class for interacting with the Airship API using either key and master secret
        or key and application secret, depending on need.

    :param key: [required] An Airship app key (project key) which identifies the project
    :param secret: [required] An Airship application secret or master secret used to
        authenticate.
    :param location: [optional] The Airship cloud site the project is located in.
        May be 'us' or 'eu'. Defaults to 'us'.
    :param timeout: [optional]  An integer specifying the number of seconds used
        for a response timeout threshold
    :param retries: [optional] An integer specifying the number of times to retry a
        failed request. Retried requests use exponential backoff between requests.
        Defaults to 0, no retry.
    """

    def __init__(
        self,
        key: str,
        secret: str,
        location: str = "us",
        timeout: int = DEFAULT_REQ_TIMEOUT_S,
        retries: int = 0,
    ) -> None:
        super().__init__(key=key, location=location, timeout=timeout, retries=retries)
        self.secret = secret
        self.session.auth = (self.key, self.secret)

    @property
    def secret(self) -> Optional[str]:
        return self._secret

    @secret.setter
    def secret(self, value: Optional[str]) -> None:
        if isinstance(value, str) and not VALID_KEY.match(value):
            raise ValueError("secrets must be 22 characters")
        self._secret = value


class BearerTokenClient(BaseClient):
    """
    Client class for interacting with the Airship API using bearer token authentication

    :param key: [required] An Airship app key (project key) which identifies the project
    :param token: [required]  An Airship-generated bearer token for the provided key.
    :param location: [optional] The Airship cloud site the project is located in.
        May be 'us' or 'eu'. Defaults to 'us'.
    :param timeout: [optional]  An integer specifying the number of seconds used
        for a response timeout threshold
    :param retries: [optional] An integer specifying the number of times to retry a
        failed request. Retried requests use exponential backoff between requests.
        Defaults to 0, no retry.
    """

    def __init__(
        self,
        key: str,
        token: str,
        location: str = "us",
        timeout: int = DEFAULT_REQ_TIMEOUT_S,
        retries: int = 0,
    ) -> None:
        super().__init__(key=key, location=location, timeout=timeout, retries=retries)
        self.token = token

        self.session.headers.update(
            {"X-UA-Appkey": key, "Authorization": f"Bearer {self.token}"}
        )

    @property
    def token(self) -> Optional[str]:
        return self._token

    @token.setter
    def token(self, value: Optional[str]) -> None:
        self._token = value


class OAuthClient(BaseClient):
    """
    Client class for interacting with the Airship API using OAuth2 authentication with
    JWT assertion.
    Note - Not all endpoints support OAuth, and client scope may further restrict
    the endpoints available to a given client. See Airship API documentation for more.

    :param key: [required] An Airship app key (project key) which identifies the project
    :param client_id: [required] An Airship provided client id used to generate OAuth
        authentication tokens.
    :param public_key:  [required] The public key required to sign JWT assertions,
        passed as a bytestring.
    :param scope: [optional] A list of scopes to which the issued token will be entitled.
    :param ip_addr: [optional] A list of CIDR representations of valid IP addresses to
        which the issued token is restricted.
    :param location: [optional] The Airship cloud site the project is located in.
        May be 'us' or 'eu'. Defaults to 'us'.
    :param timeout: [optional]  An integer specifying the number of seconds used
        for a response timeout threshold
    :param retries: [optional] An integer specifying the number of times to retry a
        failed request. Retried requests use exponential backoff between requests.
        Defaults to 0, no retry.
    """

    def __init__(
        self,
        key: str,
        client_id: str,
        private_key: str,
        location: str = "us",
        scope: Optional[List[str]] = None,
        ip_addr: Optional[List[str]] = None,
        timeout: int = DEFAULT_REQ_TIMEOUT_S,
        retries: int = 0,
    ) -> None:
        super().__init__(key, location, timeout, retries)
        self.key = key
        self.client_id = client_id
        self.scope = scope
        self.ip_addr = ip_addr
        self.private_key = private_key
        self.token_url: str = (
            f"{US_OAUTH_URL if self.location == 'us' else EU_OAUTH_URL}/token"
        )
        self.token: Optional[str] = None
        self.urls = Urls(location=self.location, oauth_base=True)
        self.access_token_expires_at: int = 0

    def _update_session_oauth_token(self) -> None:
        @backoff.on_exception(
            backoff.expo,
            (Timeout, ConnectionError),
            max_tries=5,
        )
        def _get_or_refresh_token() -> None:
            assertion_expires_at = int(time.time()) + DEFAULT_ASSERTION_EXPIRY
            headers = {
                "alg": "ES384",
                "kid": self.client_id,
            }
            claims = {
                "aud": self.token_url,
                "exp": assertion_expires_at,
                "iat": int(time.time()),
                "iss": self.client_id,
                "nonce": str(uuid.uuid4()),
                "sub": f"app:{self.key}",
            }
            if self.scope:
                claims["scope"] = self.scope
            if self.ip_addr:
                claims["ipaddr"] = self.ip_addr

            encoded_jwt = jwt.encode(
                payload=claims,
                key=self.private_key,
                algorithm="ES384",
                headers=headers,
            )

            resp = requests.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "assertion": encoded_jwt,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                },
                timeout=60,
            )
            resp_data = resp.json()
            self.token = resp_data.get("access_token")
            self.access_token_expires_at = int(time.time()) + int(
                resp_data.get("expires_in")
            )
            self.session.headers.update(
                {"X-UA-Appkey": self.key, "Authorization": f"Bearer {self.token}"}
            )

        if not self.token:
            logger.debug("No OAuth2 access token found. Getting new token.")
            return _get_or_refresh_token()

        if self.access_token_expires_at < int(time.time()):
            logger.debug("OAuth access token expired. Refreshing token.")
            return _get_or_refresh_token()

    def _request(
        self,
        method: str,
        body: Any,
        url: str,
        content_type: Optional[str] = None,
        version: int = DEFAULT_API_VERSION,
        params: Optional[Dict[str, Any]] = None,
        encoding: Optional[str] = None,
    ) -> requests.Response:
        self._update_session_oauth_token()
        return super()._request(
            method, body, url, content_type, version, params, encoding
        )
