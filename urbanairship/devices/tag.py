import json
import logging
from typing import Dict, Optional, List, Any

from urbanairship import Airship

logger = logging.getLogger("urbanairship")


class ChannelTags(object):
    """Modify the tags for a channel

    :param airship: An urbanairship.Airship instance.
    """

    def __init__(self, airship: Airship) -> None:
        self.url = airship.urls.get("channel_url") + "tags/"
        self._airship = airship
        self.audience: Dict[str, Any] = {}
        self.add_group: Dict[str, Any] = {}
        self.remove_group: Dict[str, Any] = {}
        self.set_group: Dict[str, Any] = {}

    def set_audience(
        self,
        user_ids: Optional[List[str]] = None,
        ios: Optional[str] = None,
        android: Optional[str] = None,
        amazon: Optional[str] = None,
        web: Optional[str] = None,
    ) -> None:
        """Sets the audience to be modified
        :param ios: an ios channel
        :param android: an android channel
        :param amazon: an amazon channel
        :param web: a web channel
        """
        if ios is not None:
            self.audience["ios_channel"] = ios
        if android is not None:
            self.audience["android_channel"] = android
        if amazon is not None:
            self.audience["amazon_channel"] = amazon
        if web is not None:
            self.audience["channel"] = web

    def add(self, group_name: str, tags: List[str]) -> None:
        """Sets group and tags to add

        :param group_name: The name of the tag group to add
        :param tags: The tags to add
        """
        self.add_group[group_name] = tags

    def remove(self, group_name: str, tags: List[str]) -> None:
        """Sets group and tags to remove

        :param group_name: The name of the tag group to remove
        :param tags: The tags to addremove
        """
        self.remove_group[group_name] = tags

    def set(self, group_name: str, tags: List[str]) -> None:
        """
        Sets group and tags to set. Note that a ``set`` operation replaces all tags on the audience upon send.

        :param group_name: The name of the tag group to set
        :param tags: The tags to set
        """
        self.set_group[group_name] = tags

    def send(self) -> Dict:
        """Perform the Channel Tag operations.

        :returns: JSON response from the API
        """
        payload = {}

        if not self.audience:
            raise ValueError("A audience is required for modifying tags")
        payload["audience"] = self.audience

        if self.add_group:
            if self.set_group:
                raise ValueError(
                    'A tag request cannot contain both an "add"' ' and a "set" field.'
                )
            payload["add"] = self.add_group

        if self.remove_group:
            if self.set_group:
                raise ValueError(
                    'A tag request cannot contain both a "remove"' ' and a "set" field.'
                )
            payload["remove"] = self.remove_group

        if self.set_group:
            payload["set"] = self.set_group

        if not self.add_group and not self.remove_group and not self.set_group:
            raise ValueError("An add, remove, or set field was not set")

        body = json.dumps(payload)
        response = self._airship._request(
            "POST", body, self.url, "application/json", version=3
        )
        return response.json()


class OpenChannelTags(object):
    """Modify the tags for an open channel"""

    def __init__(self, airship: Airship) -> None:
        self.url = airship.urls.get("open_channel_url") + "tags/"
        self._airship = airship
        self.audience: Dict = {}
        self.add_group: Dict = {}
        self.remove_group: Dict = {}
        self.set_group: Dict = {}

    def set_audience(self, address: str, open_platform: str) -> None:
        """Sets the audience to be modified.

        :param address: the open channel to be modified
        :param open_platform: the name of the open platform the channel belongs to.
        """
        self.audience = {"address": address, "open_platform_name": open_platform}

    def add(self, group_name: str, tags: List[str]) -> None:
        """Sets group and tags to add

        :param group_name: The name of the tag group to add
        :param tags: The tags to add
        """
        self.add_group[group_name] = tags

    def remove(self, group_name: str, tags: List[str]) -> None:
        """Sets group and tags to remove

        :param group_name: The name of the tag group to remove
        :param tags: The tags to addremove
        """
        self.remove_group[group_name] = tags

    def set(self, group_name: str, tags: List[str]) -> None:
        """
        Sets group and tags to set. Note that a ``set`` operation replaces all tags on the audience upon send.

        :param group_name: The name of the tag group to set
        :param tags: The tags to set
        """
        self.set_group[group_name] = tags

    def send(self) -> Dict:
        """Perform the Open Channel Tag operations.

        :returns: JSON response from the API
        """
        payload = {}

        if not self.audience:
            raise ValueError("An audience is required to modify tags")
        payload["audience"] = self.audience

        if not self.add_group and not self.remove_group and not self.set_group:
            raise ValueError("An add, remove, or set field was not set")

        if self.set_group:
            if self.add_group or self.remove_group:
                raise ValueError(
                    'A "set" tag request cannot contain "add" or "remove" fields'
                )
            payload["set"] = self.set_group

        if self.add_group:
            payload["add"] = self.add_group

        if self.remove_group:
            payload["remove"] = self.remove_group

        body = json.dumps(payload)
        response = self._airship._request(
            "POST", body, self.url, "application/json", version=3
        )
        return response.json()
