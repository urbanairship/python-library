import json
import logging
import re

logger = logging.getLogger('urbanairship')

VALID_EMAIL = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
VALID_ISO_8601 = re.compile(
    '^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])'
    'T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z)?$'
    )


class Email(object):
    """Register and uninstall an Email object.

    Please see the email documentation for important information about
    opt-in times and email types.
    https://docs.urbanairship.com/api/ua/#operation/api/channels/email

    :param address: Required. The email address the object represents.
    :param commercial_opted_in: Optional. A string in ISO 8601 format that
        represents the time explicit permission was received from the user
        to accept commercial emails.
    :param commercial_opted_out: Optional. A string in ISO 8601 format that
        represents the time a user opted out of commercial emails.
    :param transactional_opted_in: Optional. A string in ISO 8601 format
        that represents the time a user explicitly opted in to transactional
        emails.
    :param transactional_opted_out: Optional. A string in ISO 8601 formation
        that represents the time a user explicitly opted out of transactional
        emails.
    :param locale_country: Optional. The device property tag related
        to locale country setting.
    :param locale_language: Optional. The device property tag related
        to locale language setting.
    :param timezone: Optional. The deice property tag related to
        timezone setting.
    :param template_fields: For use with CreateAndSend with inline templates.
        A dict of template field names and their substitution values.
    """

    def __init__(self, airship, address, commercial_opted_in=None,
                 commercial_opted_out=None, transactional_opted_in=None,
                 transactional_opted_out=None, locale_country=None,
                 locale_language=None, timezone=None, template_fields=None):
        self.airship = airship
        self.address = address
        self.commercial_opted_in = commercial_opted_in
        self.commercial_opted_out = commercial_opted_out
        self.transactional_opted_in = transactional_opted_in
        self.transactional_opted_out = transactional_opted_out
        self.locale_country = locale_country
        self.locale_language = locale_language
        self.timezone = timezone
        self.template_fields = template_fields
        self._email_type = 'email'  # only acceptable value at this time
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
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not VALID_EMAIL.match(value) and value is not None:
            raise ValueError('Invalid email address')
        self._address = value

    @property
    def commercial_opted_in(self):
        return self._commercial_opted_in

    @commercial_opted_in.setter
    def commercial_opted_in(self, value):
        if value is not None and not VALID_ISO_8601.match(value):
            raise ValueError('Must use ISO 8601 timestamp format')
        self._commercial_opted_in = value

    @property
    def commercial_opted_out(self):
        return self._commercial_opted_out

    @commercial_opted_out.setter
    def commercial_opted_out(self, value):
        if value is not None and not VALID_ISO_8601.match(value):
            raise ValueError('Must use ISO 8601 timestamp format')
        self._commercial_opted_out = value

    @property
    def transactional_opted_in(self):
        return self._transactional_opted_in

    @transactional_opted_in.setter
    def transactional_opted_in(self, value):
        if value is not None and not VALID_ISO_8601.match(value):
            raise ValueError('Must use ISO 8601 timestamp format')
        self._transactional_opted_in = value

    @property
    def transactional_opted_out(self):
        return self._transactional_opted_out

    @transactional_opted_out.setter
    def transactional_opted_out(self, value):
        if value is not None and not VALID_ISO_8601.match(value):
            raise ValueError('Must use ISO 8601 timestamp format')
        self._transactional_opted_out = value

    @property
    def create_and_send_audience(self):
        audience = {
            'ua_address': self.address,
        }
        if self.commercial_opted_in:
            audience['ua_commercial_opted_in'] = self.commercial_opted_in
        if self.transactional_opted_in:
            audience['ua_transactional_opted_in'] = self.transactional_opted_in
        if self.template_fields:
            audience.update(self.template_fields)

        return audience

    def register(self):
        """Create a new email channel or unsubscribe an existing email
        channel from receiving commercial emails.
        To unsubscribe an existing channel, set email_opt_in_level
        to none.

        :return: The response object from the API.
        """
        url = self.airship.urls.get('email_url')
        reg_payload = {
            'channel': {
                'type': self._email_type,
                'address': self.address,
            }
        }

        if self.commercial_opted_in:
            reg_payload['channel']['commercial_opted_in'] = \
                self.commercial_opted_in
        if self.commercial_opted_out:
            reg_payload['channel']['commercial_opted_out'] = \
                self.commercial_opted_out
        if self.transactional_opted_in:
            reg_payload['channel']['transactional_opted_in'] = \
                self.transactional_opted_in
        if self.transactional_opted_out:
            reg_payload['channel']['transactional_opted_out'] = \
                self.transactional_opted_out

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

        url = self.airship.urls.get('email_uninstall_url')
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
        self.url = airship.urls.get('email_tags_url')
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
