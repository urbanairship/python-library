import json
import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')


class ChannelUninstall(object):
    _airship = None
    url = common.CHANNEL_URL + 'uninstall/'

    def __init__(self, airship):
        self._airship = airship

    def uninstall(self, channels):
        chan_num = len(channels)

        if chan_num > 200:
            print("Maximum of 200 channel uninstalls exceeded. ({} channels)"
                  .format(chan_num))
            return

        body = json.dumps(channels)
        response = self._airship._request('POST', body, self.url, version=3)
        logger.info("Successfully uninstalled {} channels".format(chan_num))
        return response