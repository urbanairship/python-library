import json
import logging
import re

logger = logging.getLogger('urbanairship')

VALID_MSISDN = re.compile(r'[0-9]*$')
VALID_SENDER = re.compile(r'[0-9]*$')


class Sms(object):
    """
    Create, register, opt-out and uninstall an Sms object.

    :param airship: Required. An urbanairship.Airship object instantiated with
        master authentication.
    :param sender: Required. The a number that recipients will recieve SMS
        notifications from. This must match your Urban Airship configuration.
    :param msisdn: Required. The mobile phone number you want to register as
        an SMS channel (or send a request to opt-in).
    :param opted_in: The UTC datetime in ISO 8601 format that represents the
        date and time when explicit permission was received from the user to
        receive messages. This is required for use with CreateAndSend.
    :param template_fields: For use with CreateAndSend with inline templates.
        A dict of template field names and their substitution values.
    """

    def __init__(self, airship, sender, msisdn, opted_in=False, template_fields=None):
        self.airship = airship
        self.sender = sender
        self.msisdn = msisdn
        self.opted_in = opted_in
        self.template_fields = template_fields
        self.channel_id = None

    @property
    def template_fields(self):
        return self._template_fields

    @template_fields.setter
    def template_fields(self, value):
        if not isinstance(value, (dict, type(None))):
            raise TypeError('template_fields must be a dict')

        self._template_fields = value

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

    @property
    def create_and_send_audience(self):
        audience = {
            'ua_sender': self.sender,
            'ua_msisdn': self.msisdn,
        }

        if self.template_fields:
            audience.update(self.template_fields)

        if self.opted_in:
            audience['ua_opted_in'] = self.opted_in
        else:
            raise ValueError(
                'sms objects for create and send must include opt-in datestamps'
                )
        return audience

    def register(self, opted_in=False):
        """Register an Sms channel with the sender ID and MSISDN

        :param opted_in: Optional UTC ISO 8601 datetime string that represents the
            date and time when explicit permission was received from the
            user to receive messages.

        :return: The response object from the api.
        """

        url = self.airship.urls.get('sms_url')
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

        url = self.airship.urls.get('sms_opt_out_url')

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

        url = self.airship.urls.get('sms_uninstall_url')

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

        url = self.airship.urls.get('sms_url') + '{msisdn}/{sender}'.format(
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
