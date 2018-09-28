import json
import logging
import re

from urbanairship import common

logger = logging.getLogger('urbanairship')

VALID_EMAIL = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
VALID_OPT_IN_LEVELS = ('commercial', 'transactional', 'none')


class Email(object):
    """Register and uninstall an Email object

    :param address: Required. The email address the object represents.
    :param opt_in_level: Required. The opt-in level for the email
        address. Must be one of: commercial, transactional, none.
    :param locale_country: Optional. The device property tag related
        to locale country setting.
    :param locale_language: Optional. The device property tag related
        to locale language setting.
    :param timezone: Optional. The deice property tag related to
        timezone setting."""

    def __init__(self, airship, address, opt_in_level, locale_country=None,
                 locale_language=None, timezone=None):
        self.airship = airship
        self.address = address
        self.opt_in_level = opt_in_level
        self.locale_country = locale_country
        self.locale_language = locale_language
        self.timezone = timezone
        self.email_type = 'email'  # only acceptable value at this time
        self.channel_id = None

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not VALID_EMAIL.match(value):
            raise ValueError('Invalid email address')
        self._address = value

    @property
    def opt_in_level(self):
        return self._opt_in_level

    @opt_in_level.setter
    def opt_in_level(self, value):
        if value not in VALID_OPT_IN_LEVELS:
            raise ValueError('Email opt_in_level not valid')
        self._opt_in_level = value

    def register(self):
        """Create a new email channel or unsubscribe an existing email
        channel from receiving commercial emails.
        To unsubscribe an existing channel, set email_opt_in_level
        to none.

        :return: The response object from the API.
        """
        url = common.EMAIL_URL
        reg_payload = {
            'channel': {
                'type': self.email_type,
                'email_opt_in_level': self.opt_in_level,
                'address': self.address,
            }
        }

        if self.locale_language is not None:
            reg_payload['channel']['locale_language'] = self.locale_language
        if self.locale_country is not None:
            reg_payload['channel']['locale_country'] = self.locale_country
        if self.timezone is not None:
            reg_payload['channel']['timezone'] = self.timezone

        body = json.dumps(reg_payload).encode('utf-8')

        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            version=3
        )

        if response.status_code == 201:
            self.channel_id = response.json().get('channel_id')
            logger.info(
                'Successfully created channel with channel_id %s' % (
                    self.channel_id
                )
            )
        elif response.status_code == 200:
            self.channel_id = response.json().get('channel_id')
            logger.info(
                'Successful registration call made to channel_id %s' % (
                    self.channel_id
                )
            )

        return response

    def uninstall(self):
        """Removes an email address from Urban Airship. Use with caution.
        If the uninstalled email address opts-in again, it will generate
        a new channel_id.
        The new channel_id cannot be reassociated with any opt-in
        information, tags, named users, insight reports, or other
        information from the uninstalled email channel.

        :return: The response object from the API"""

        url = common.EMAIL_UNINSTALL_URL
        uninstall_payload = {'email_address': self.address}

        body = json.dumps(uninstall_payload).encode('utf-8')

        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            version=3
        )

        logger.info('Uninstalled email address: %s' % self.address)

        return response


class EmailTags(object):
    """Add, remove or set tags for a list of email addresses"""
    def __init__(self):
        pass

    def add(self):
        pass

    def remove(self):
        pass

    def set(self):
        pass
