import json
import logging
import re

from urbanairship import common

logger = logging.getLogger('urbanairship')

VALID_MSISDN = re.compile(r'[0-9]*$')
VALID_SENDER = re.compile(r'[0-9]*$')


class Sms(object):
    """Register, opt-out and uninstall an Sms object"""

    def __init__(self, airship, sender, msisdn):
        self.airship = airship
        self.sender = sender
        self.msisdn = msisdn
        self.opted_in = False
        self.channel_id = None

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        if not VALID_SENDER.match(value):
            raise ValueError('sender must be a numeric string')
        self._sender = value

    @property
    def msisdn(self):
        return self._msisdn

    @msisdn.setter
    def msisdn(self, value):
        if not VALID_MSISDN.match(value):
            raise ValueError('msisdn must be a numeric string')
        self._msisdn = value

    @property
    def common_payload(self):
        return {
            'sender': self.sender,
            'msisdn': self.msisdn,
        }

    def register(self, opted_in=False):
        """Register an Sms channel with the sender ID and MSISDN

        :param opted_in: Optional UTC ISO 8601 datetime string that represents the
            date and time when explicit permission was received from the
            user to receive messages.

        :return: The response object from the api.
        """

        url = common.SMS_URL
        reg_payload = self.common_payload

        if opted_in:
            reg_payload['opted_in'] = opted_in

        body = json.dumps(reg_payload).encode('utf-8')

        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            version=3
        )

        if response.json().get('status') == 'pending':
            logger.info(
                'Channel creation for msisdn %s pending user opt-in' % (
                    self.msisdn
                )
            )
        elif response.json().get('channel_id') is not None:
            self.channel_id = response.json().get('channel_id')
            logger.info(
                'Successfully registered Sms channel with channel_id %s' % (
                    self.channel_id
                )
            )
        else:
            logger.info(
                'Channel not yet created.'
            )


        return response

    def opt_out(self):
        """mark an sms channel at opted-out by sender ID and MSISDN

        :return: the response object from the api
        """

        url = common.SMS_OPT_OUT_URL

        response = self.airship.request(
            method='POST',
            body=json.dumps(self.common_payload).encode('utf-8'),
            url=url,
            version=3
        )

        logger.info(
            'Opted out Sms channel with sender: %s and msisdn: %s' % (
                self.sender, self.msisdn
            )
        )

        return response

    def uninstall(self):
        """Uninstall and remove all associated data from Urban Airship
        systems. Channel cannot be opted-in again. Use with caution.

        :return: the response object from the api"""

        url = common.SMS_UNINSTALL_URL

        response = self.airship.request(
            method='POST',
            body=json.dumps(self.common_payload).encode('utf-8'),
            url=url,
            version=3
        )

        logger.info(
            'Uninstalled Sms channel with sender: %s and msisdn: %s' % (
                self.sender, self.msisdn
            )
        )

        return response

    def lookup(self):
        """Look up Sms channel information

        :return: the response object from the api
        """

        url = common.SMS_URL + '{msisdn}/{sender}'.format(
            msisdn=self.msisdn,
            sender=self.sender
        )

        response = self.airship.request(
            method='GET',
            body=None,
            url=url,
            version=3
        )

        return response
