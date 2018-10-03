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
        self._email_type = 'email'  # only acceptable value at this time
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
                'type': self._email_type,
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
    """Add, remove or set tags for a list of email addresses

    :param address: an email address to mutate tags for
    """
    def __init__(self, airship, address):
        self.airship = airship
        self.url = common.EMAIL_TAGS_URL
        self.address = address
        self.add_group = {}
        self.remove_group = {}
        self.set_group = {}
        self._payload = {}

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not VALID_EMAIL.match(value):
            raise ValueError('addresses must be and email address')
        self._address = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if not isinstance(value, list):
            raise ValueError('tags must be input as a list')
        self._tags = value

    def add(self, group, tags):
        """
        add tags to a given tag group
        :param group: the tag group to add to
        :param tags: a list of tags to add
        """
        self.add_group[group] = tags

    def remove(self, group, tags):
        """
        remove tags from a given tag group
        :param group: the tag group to remove tags from
        :param tags: a list of tags to remove
        """
        self.remove_group[group] = tags

    def set(self, group, tags):
        """
        replace all tags on the given tag group with these tags
        :param group: the tag group to set tags on
        :param tags: a list of tags to set
        """
        self.set_group[group] = tags

    def send(self):
        """
        commit add, remove and set operations. set cannot be used with
        add and remove.
        :return: the response object from the api
        """
        if not self.add_group and not self.remove_group and not self.set_group:
            raise ValueError('at least one add, remove or set group must exist')
        self._payload['audience'] = {'email_address': self.address}

        if self.set_group:
            if self.add_group or self.remove_group:
                raise ValueError('set cannot be used with remove or add groups')
            self._payload['set'] = self.set_group

        if self.add_group:
            self._payload['add'] = self.add_group

        if self.remove_group:
            self._payload['remove'] = self.remove_group

        body = json.dumps(self._payload).encode('utf-8')

        response = self.airship.request(
            method='POST',
            body=body,
            url=self.url,
            version=3
        )

        return response
