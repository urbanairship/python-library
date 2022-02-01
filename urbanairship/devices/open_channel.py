import datetime
import json
import logging
import re
from typing import Any, Optional, Dict, List

from requests import Response

from urbanairship import Airship

VALID_UUID = re.compile(r"[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z")

logger = logging.getLogger("urbanairship")


class OpenChannel(object):
    """
    Represents an open channel.

    :param channel_id: The Airship generated channel_id value for the open channel
    :param address: The open channel's address
    :param open_platform: The open platform associated with the channel
    """

    channel_id: Optional[str] = None
    address: Optional[str] = None
    open_platform: Optional[str] = None
    identifiers: Optional[str] = None
    opt_in: Optional[bool] = None
    installed: Optional[bool] = None
    created: Optional[str] = None
    last_registration: Optional[str] = None
    tags: Optional[List] = None
    template_fields: Optional[Dict] = None

    def __init__(self, airship: Airship) -> None:
        self.airship = airship

    @property
    def create_and_send_audience(self) -> Dict:
        if not self.address:
            raise ValueError("open channel address must be set")

        audience = {"ua_address": self.address}

        if self.template_fields:
            audience.update(self.template_fields)

        return audience

    def create(self) -> Response:
        """Create this OpenChannel object with the API."""

        if not self.address:
            raise ValueError("Must set address before creation.")

        if not self.open_platform:
            raise ValueError("Must set open_platform before creation.")

        if not isinstance(self.opt_in, bool):
            raise ValueError("Must set opt_in before creation.")

        if self.tags and not isinstance(self.tags, list):
            raise TypeError('"tags" must be a list')

        url = self.airship.urls.get("open_channel_url")

        channel_data: Dict[str, Any] = {
            "type": "open",
            "address": self.address,
            "opt_in": self.opt_in,
            "open": {"open_platform_name": self.open_platform},
        }

        if self.tags:
            channel_data["tags"] = self.tags
        if self.identifiers:
            channel_data["open"]["identifiers"] = self.identifiers

        body = json.dumps({"channel": channel_data})
        response = self.airship.request(method="POST", body=body, url=url, version=3)

        self.channel_id = response.json().get("channel_id")

        logger.info(
            "Successful open channel creation: %s (%s)", self.channel_id, self.address
        )

        return response

    def update(self) -> Response:
        """Update this OpenChannel object."""

        if not self.address and not self.channel_id:
            raise ValueError("Must set address or channel ID to update.")

        if not self.open_platform:
            raise ValueError("Must set open_platform.")

        if not isinstance(self.opt_in, bool):
            raise ValueError("Must set opt_in.")

        if not self.address and self.opt_in is True:
            raise ValueError("Address must be set for opted in channels.")

        url = self.airship.urls.get("open_channel_url")

        channel_data: Dict[str, Any] = {
            "type": "open",
            "open": {"open_platform_name": self.open_platform},
            "opt_in": self.opt_in,
        }
        if self.channel_id:
            channel_data["channel_id"] = self.channel_id
        if self.address:
            channel_data["address"] = self.address
        if self.tags:
            channel_data["tags"] = self.tags
        if self.identifiers:
            channel_data["open"]["identifiers"] = self.identifiers

        body = json.dumps({"channel": channel_data})
        response = self.airship.request(method="POST", body=body, url=url, version=3)

        self.channel_id = response.json().get("channel_id")

        logger.info(
            "Successful open channel update: %s (%s)", self.channel_id, self.address
        )

        return response

    @classmethod
    def from_payload(cls, payload: Dict, airship: Airship):
        """Instantiate an OpenChannel from a payload."""
        obj = cls(airship)
        for key in payload:
            # Extract the open channel data
            if key == "open":
                obj.open_platform = payload["open"].get("open_platform_name")
                obj.identifiers = payload["open"].get("identifiers", [])
                continue

            if key in ("created", "last_registration"):
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], "%Y-%m-%dT%H:%M:%S"
                    )
                except (KeyError, ValueError):
                    payload[key] = "UNKNOWN"
            setattr(obj, key, payload[key])

        return obj

    def lookup(self, channel_id: str):
        """Retrieves an open channel from the provided channel ID."""
        url = self.airship.urls.get("channel_url") + channel_id
        response = self.airship._request(method="GET", body=None, url=url, version=3)
        payload = response.json().get("channel")

        return self.from_payload(payload, self.airship)

    def uninstall(self) -> Response:
        """Mark this OpenChannel object uninstalled"""
        url = self.airship.urls.get("open_channel_url") + "uninstall/"
        if self.address is None or self.open_platform is None:
            raise ValueError('"address" and "open_platform" are required attributes')

        channel_data = {
            "address": self.address,
            "open_platform_name": self.open_platform,
        }

        body = json.dumps(channel_data)
        response = self.airship.request(method="POST", body=body, url=url, version=3)

        logger.info(
            "Successfully uninstalled open channel %s"
            % channel_data["open_platform_name"]
        )

        return response
