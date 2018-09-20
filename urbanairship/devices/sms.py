import json
import logging

from urbanairship import common

logger = logging.getLogger('urbanairship')


class SMS(object):
    """Register, opt-out and uninstall an SMS object"""

    def __init__(self, airship, sender=None, msisdn=None):

        self.airship = airship

        if sender is None:
            raise ValueError('Must set sms sender id for creation')

        if msisdn is None:
            raise ValueError('Must set msisdn for creation')

        self.sender = sender
        self.msisdn = msisdn
        self.common_payload = {
            'sender': sender,
            'msisdn': msisdn
        }

    def register(self, opted_in=None):
        """Register an SMS channel with the sender id and msisdn

        :param opted_in: Optional UTC IOS 8601 datetime string that represents the
            date and time when explicit permission was received from the
            user to receive messages.

        :return: The response object from the api.
        """

        url = common.SMS_URL

        if opted_in:
            self.common_payload['opted_in'] = opted_in

        body = json.dumps(self.common_payload).encode('utf-8')

        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            version=3
        )

        if opted_in is not None:
            self.channel_id = response.json().get('channel_id')
            logger.info(
                'Successfully registered SMS channel with channel_id %s' % (
                    self.channel_id
                )
            )
        else:
            self.channel_id = None
            logger.info(
                'Channel creation for msisdn %s pending user opt-in' % (
                    self.msisdn
                )
            )

        return response

    def opt_out(self):
        """mark an sms channel by sender and msisdn

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
            'Opted out SMS channel with sender: %s and msisdn: %s' % (
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
            'Uninstalled SMS channel with sender: %s and msisdn: %s' % (
                self.sender, self.msisdn
            )
        )

        return response

    def lookup(self):
        """lookup SMS channel information

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
