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
            raise ValueError(
                ('Maximum of 200 channel uninstalls exceeded. '
                 '({0} channels)').format(chan_num)
            )

        body = json.dumps(channels)
        response = self._airship._request('POST', body, self.url, version=3)
        logger.info('Successfully uninstalled {0} channels'.format(chan_num))
        return response


class OpenChannelUninstall(object):
    _airship = None
    url = common.OPEN_CHANNEL_URL + 'uninstall/'

    def __init__(self, airship):
        self._airship = airship

    def uninstall(self, channel):
        '''Uninstall open channel without a channel id

        :keyword channel: Required open channel identifier containing
            two attributes - "address" and "open_platform_name"

        >>> channel = {
            "address": "new_email@example.com",
            "open_platform_name": "email"
            }
        >>> uninstall(channel)
        {
            "ok": true
        }
        '''

        if not isinstance(channel, dict):
            raise TypeError(
                'Open channel identifier must be a dictionary'
            )
        if not ('address' in channel or 'open_platform_name' in channel):
            raise ValueError(
                'Open channel identifier must include attributes '
                '"address" and "open_platform_name"'
            )

        body = json.dumps(channel)
        response = self._airship._request(
                            'POST',
        body, self.url, version=3)
        logger.info(
            'Successfully uninstalled open channel {0}'.format(channel['open_platform_name'])
        )
        return response
