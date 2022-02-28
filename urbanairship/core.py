import logging
import re
import warnings
from typing import Optional, Dict, Any

import backoff  # type: ignore
import requests

from . import __about__, common
import urbanairship

logger = logging.getLogger("urbanairship")

VALID_KEY = re.compile(r"^[\w-]{22}$")
VALID_LOCATIONS = ["eu", "us", None]


class Urls(object):
    def __init__(self, location: Optional[str] = None) -> None:
        if not location or location.lower() == "us":
            self.base_url = "https://go.urbanairship.com/api/"
        elif location.lower() == "eu":
            self.base_url = "https://go.airship.eu/api/"

        self.channel_url = self.base_url + "channels/"
        self.open_channel_url = self.channel_url + "open/"
        self.device_token_url = self.base_url + "device_tokens/"
        self.apid_url = self.base_url + "apids/"
        self.push_url = self.base_url + "push/"
        self.validate_url = self.push_url + "validate/"
        self.schedules_url = self.base_url + "schedules/"
        self.tags_url = self.base_url + "tags/"
        self.segments_url = self.base_url + "segments/"
        self.reports_url = self.base_url + "reports/"
        self.lists_url = self.base_url + "lists/"
        self.attributes_url = self.channel_url + "attributes/"
        self.attributes_list_url = self.base_url + "attribute-lists/"
        self.message_center_delete_url = self.base_url + "user/messages/"
        self.subscription_lists_url = self.channel_url + "subscription_lists/"
        self.templates_url = self.base_url + "templates/"
        self.schedule_template_url = self.templates_url + "schedules/"
        self.pipelines_url = self.base_url + "pipelines/"
        self.named_user_url = self.base_url + "named_users/"
        self.named_user_tag_url = self.named_user_url + "tags/"
        self.named_user_disassociate_url = self.named_user_url + "disassociate/"
        self.named_user_associate_url = self.named_user_url + "associate/"
        self.named_user_uninstall_url = self.named_user_url + "uninstall/"
        self.sms_url = self.channel_url + "sms/"
        self.sms_opt_out_url = self.sms_url + "opt-out/"
        self.sms_uninstall_url = self.sms_url + "uninstall/"
        self.sms_custom_response_url = self.base_url + "sms/custom-response/"
        self.email_url = self.channel_url + "email/"
        self.email_tags_url = self.email_url + "tags/"
        self.email_uninstall_url = self.email_url + "uninstall/"
        self.create_and_send_url = self.base_url + "create-and-send/"
        self.schedule_create_and_send_url = self.schedules_url + "create-and-send/"
        self.experiments_url = self.base_url + "experiments/"
        self.experiments_schedule_url = self.experiments_url + "scheduled/"
        self.experiments_validate = self.experiments_url + "validate/"
        self.attachment_url = self.base_url + "attachments/"
        self.custom_events_url = self.base_url + "custom-events/"
        self.tag_lists_url = self.base_url + "tag-lists/"

    def get(self, endpoint: str) -> str:
        url: str = getattr(self, endpoint)

        if not url:
            raise AttributeError("No url for endpoint %s" % endpoint)

        return url


class Airship(object):
    def __init__(
        self,
        key: str,
        secret: Optional[str] = None,
        token: Optional[str] = None,
        location: str = "us",
        timeout: Optional[int] = None,
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
        :param retries: [optional] An integer specifying the number of times to retry a
        failed request. Retried requests use exponential backoff between requests.
        Defaults to 0, no retry.
        """
        self.key: str = key
        self.secret: Optional[str] = secret
        self.token: Optional[str] = token
        self.location: str = location
        self.timeout: Optional[int] = timeout
        self.retries = retries
        self.urls: Urls = Urls(self.location)

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
            headers["Accept"] = (
                "application/vnd.urbanairship+json; " "version=%d;" % version
            )
        if encoding:
            headers["Content-Encoding"] = encoding

        @backoff.on_exception(
            backoff.expo, common.AirshipFailure, max_tries=(self.retries + 1)
        )
        def make_retryable_request(
            method: str,
            url: str,
            body: Any,
            params: Optional[Dict[str, Any]],
            headers: Dict[str, Any],
        ) -> requests.Response:
            response: requests.Response = self.session.request(
                method,
                url,
                data=body,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )

            logger.debug(
                "Making %s request to %s. Headers:\n\t%s\nBody:\n\t%s",
                method,
                url,
                "\n\t".join(
                    "%s: %s" % (key, value) for (key, value) in headers.items()
                ),
                body,
            )

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

    def create_push(self):
        """Create a Push notification."""
        warnings.warn(
            category=DeprecationWarning,
            message="the create_push function is deprecated. please use urbanairship.Push. This will be removed in version 7.0",
        )
        return urbanairship.Push(self)

    def create_scheduled_push(self):
        """Create a Scheduled Push notification."""
        warnings.warn(
            category=DeprecationWarning,
            message="the create_scheduled_push function is deprecated. please use urbanairship.ScheduledPush. This will be removed in version 7.0",
        )
        return urbanairship.ScheduledPush(self)

    def create_template_push(self):
        """Create a Scheduled Push notification."""
        warnings.warn(
            category=DeprecationWarning,
            message="the create_template_push function is deprecated. please use urbanairship.TemplatePush. This will be removed in version 7.0",
        )
        return urbanairship.TemplatePush(self)
