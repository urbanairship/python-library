import json
import logging
from typing import List

from requests import Response

from urbanairship import Airship

logger = logging.getLogger("urbanairship")


class ChannelUninstall(object):
    """
    Uninstalls a channel id.

    :param airship: Required. An urbanairship.Airship instance
    """

    def __init__(self, airship: Airship) -> None:
        self._airship = airship

    def uninstall(self, channels: List[str]) -> Response:
        """
        Perform the channel unistall on a list of channel UUIDs.

        :param channels: Required. A list of channel_id UUIDs.
        """
        chan_num: int = len(channels)

        if chan_num > 200:
            raise ValueError(
                ("Maximum of 200 channel uninstalls exceeded. ({0} channels)").format(
                    chan_num
                )
            )

        body = json.dumps(channels)
        url = self._airship.urls.get("channel_url") + "uninstall/"

        response = self._airship._request("POST", body, url, version=3)
        logger.info("Successfully uninstalled {0} channels".format(chan_num))

        return response
