import logging
import json

import uareach as ua
from uareach import common, util
from uareach.templates import Template


logger = logging.getLogger(__name__)

class PassMetadata(util.Constant):
    PUBLIC_URL = 'publicUrl'
    PASS_ID = 'pass_id'
    TEMPLATE_ID = 'template_id'


def get_pass(reach, pass_id=None, external_id=None):
    """Retrieve a pass.

    Args:
        reach (reach.core.Reach): A uareach client object.
        pass_id (str): The pass ID of the pass you wish to retrieve.
        pass_external_id (str): The external ID of the pass you wish to
        retrieve.

    Returns:
        An ApplePass or GooglePass object.

    Example:
        >>> my_pass = Pass.get_pass(pass_external_id=12345)
        <id:67890745, templateId:51010>
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = reach.request(
        method='GET',
        body=None,
        url=Pass.build_url(
            common.PASS_BASE_URL,
            main_id=pass_id,
            pass_external_id=external_id
        ),
        version=1.2
    )
    return _pass_dispatch(response.json())


def _pass_dispatch(data):
    """Infer the pass vendor based on field type.
    """
    fields = data.get('fields')
    for name, field_data in fields.iteritems():
        field_type = field_data['fieldType']
        if field_type == 'notAssigned':
            continue
        try:
            ua.AppleFieldType.validate(field_type)
            return ApplePass.from_data(data)
        except ValueError:
            try:
                ua.GoogleFieldType.validate(field_type)
                return GooglePass.from_data(data)
            except ValueError:
                pass
    raise ValueError("Unrecognized pass structure.")


def delete_pass(reach, pass_id=None, external_id=None):
    """Delete a pass.

    Arguments:
        reach (reach.Reach): A UA uareach object.
        pass_id (str or int): The ID of the pass you wish to delete.
        external_id (str or int): The external ID of the pass you wish
            to delete.

    Returns:
        A boolean representing success.

    Raises:
        ValueError: If neither, or both, of pass_id and external_id
            are specified.

    Example:
        >>> delete_pass(uareach, pass_id='123456')
        True
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = reach.request(
        method='DELETE',
        body=None,
        url=Pass.build_url(
            common.PASS_BASE_URL,
            main_id=pass_id,
            pass_external_id=external_id
        ),
        version=1.2
    )
    logger.info('Successful pass deletion: {}'.format(
        pass_id if pass_id else external_id
    ))
    return True


def add_pass_locations(reach, locations, pass_id=None, external_id=None):
    """Add locations to a pass.

    Arguments:
        reach (reach.core.Reach): A uareach client object.
        locations (list): A list of dictionaries representing location
            objects.
        pass_id (str): The ID of the pass you wish to add
            locations to.
        external_id (str): The external ID of the pass you wish to add
            locations to.

    Returns:
        A list of objects containing the location value and passLocationId.

    Raises:
        ValueError: If neither, or both of, pass_id and external_id
            are specified.

    Example:
        >>> add_locations(ua_reach, location1, location2, pass_id=12345)
        True
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = reach.request(
        method='POST',
        body=json.dumps({"locations": locations}),
        url=Pass.build_url(
            common.PASS_ADD_LOCATION_URL,
            main_id=pass_id,
            pass_external_id=external_id
        ),
        content_type='application/json',
        version=1.2
    )
    logger.info('Successfully added {} locations to pass {}.'.format(
        len(locations),
        pass_id if pass_id else external_id
    ))
    return response.json()


def delete_pass_location(reach, location_id, pass_id=None, external_id=None):
    """Delete a location from a pass.

    Arguments:
        reach (reach.core.Reach): A uareach client object.
        location_id (str or int): The ID of the location you wish to delete.
        pass_id (str or itn): The ID of the pass you wish to delete
            locations from.
        external_id (str or int): The external ID of the pass you wish
            to delete locations from.

    Returns:
        A boolean representing success.

    Raises:
        ValueError: If both or neither of pass_id and external_id are
            specified.

    Example:
        >>> delete_location(ua_reach, 12345, pass_id=44444)
        True
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = reach.request(
        method='DELETE',
        body=None,
        url=Pass.build_url(
            common.PASS_DELETE_LOCATION_URL,
            main_id=pass_id,
            pass_external_id=external_id,
            location_id=location_id
        ),
        version=1.2
    )
    logger.info('Successfully deleted location {} from pass {}.'.format(
        location_id,
        pass_id if pass_id else external_id
    ))
    return True


class PassList(common.IteratorParent):
    """Forms a pass listing request.

    Arguments:
        reach (reach.core.Reach): The uareach client object.
        template_id (int): An integer ID specifing the template you would like to
            retrieve passes from.
        status (string): An optional string, can be one of ``"installed"``,
            ``"uninstalled"``, ``"been_installed"``, and ``"not_been_installed"``.
        page_size (int): The size of each page of the pass listing
            response. Defaults to 10.
        page (int): The page to start the listing response on. Defaults
            to 1.
        order (string): The attribute used to order the passes. Can be one
            of ``"id"``, ``"name"``, ``"createdAt"``, or ``"updatedAt"``.
            Defaults to ``"id"``.
        direction (string): The direction of the pass list, can be one of
            ``"ASC"`` or ``"DESC"``. Defaults to ``"DESC"``.

    Example:
        >>> pass_list = PassList(ua_reach)
        >>> for item in pass_list:
        ...     print item['createdAt']
        ...
        2016-07-27T21:14:47Z
        2016-07-23T12:13:32Z
        2016-06-09T17:32:14Z
    """
    base_url = common.PASS_BASE_URL.format('')
    data_attribute = 'passes'

    def __init__(
        self,
        reach,
        status=None,
        template_id=None,
        page_size=None,
        page=None,
        order=None,
        direction=None
    ):

        if direction not in {None, 'ASC', 'DESC'}:
            raise ValueError(
                'Unrecognized direction "{}". '
                'Please use one of "ASC" or "DESC"'.format(direction)
            )

        statuses = {
            'installed',
            'uninstalled',
            'been_installed',
            'not_been_installed'
        }

        if not (status is None or status in statuses):
            raise ValueError(
                "Unrecognized status '{}'. "
                "Please use one of {}.".format(status, statuses)
            )

        params = {
            'status': status,
            'templateId': template_id,
            'pageSize': page_size,
            'page': page,
            'order': order,
            'direction': direction
        }

        params = {k: v for k, v in params.iteritems() if v is not None}
        super(PassList, self).__init__(reach, params)


@util.inherit_docs
class Pass(Template):

    METADATA = ['publicUrl']
    READ_ONLY_METADATA = [
        'url', 'status', 'updatedAt', 'pass_id', 'template_id', 'createdAt', 'serialNumber', 'tags'
    ]

    def create(self, reach, template_id=None, template_ext_id=None, pass_ext_id=None):
        """Create a pass.

        Arguments:
            reach (reach.core.Reach): A uareach client object.
            template_id (str/int): A template ID.
            template_ext_id (str/int): A template external ID.
            pass_ext_id (str/int): A pass external ID.

        Returns:
            A dictionary containing ``'id'`` and ``'url'`` keys.

        Raises:
            ValueError: If neither, or both, of template_id and template_ext_id
                are specified.

        Example:
            >>> my_pass.create(ua_reach, project_id=12345)
            {'id': 123456, 'url': 'https://blah.com'}
        """
        if template_id and template_ext_id:
            raise ValueError(
                "'template_id' and 'template_ext_id' cannot both be set"
            )

        response = reach.request(
            method='POST',
            body=json.dumps(self._create_payload()),
            url=Pass.build_url(
                common.PASS_BASE_URL,
                main_id=template_id,
                template_external_id=template_ext_id,
                pass_external_id=pass_ext_id
            ),
            content_type='application/json',
            version=1.2
        )
        pass_id = response.json()['id']
        logger.info('Successful pass creation: {}'.format(
            pass_id if pass_id else pass_ext_id
        ))
        self.metadata['id'] = pass_id
        return {'id': pass_id, 'url': response.json()['url']}

    def update(self, reach, pass_id=None, external_id=None):
        """Update a pass.

        Arguments:
            reach (reach.core.Reach): A uareach client object.
            pass_id (str): ID of the pass to update.
            external_id (str): External ID of the pass to update.

        Returns:
            A dictionary containing a ticketId.

        Raises:
            ValueError: If neither, or both, of pass_id and external_id
                are specified.

        Example:
            >>> my_pass.update(ua_reach)
            {'ticketId': 4125123}
        """
        if pass_id and external_id:
            raise ValueError("'pass_id' and 'external_id' cannot both be set")

        if not (pass_id or external_id):
            pass_id = self.metadata.get('id', None)
            if not pass_id:
                raise ValueError(
                    "Either set pass_id or external_id when "
                    "calling update, or set the pass 'id' attribute."
                )

        response = reach.request(
            method='PUT',
            body=json.dumps(self._create_payload()),
            url=Pass.build_url(
                common.PASS_BASE_URL,
                main_id=pass_id,
                template_external_id=external_id
            ),
            content_type='application/json',
            version=1.2
        )
        logger.info('Successful pass update: {}'.format(
            pass_id if pass_id else external_id
        ))
        return response.json()

    @classmethod
    def from_data(cls, data):
        pass_ = cls()

        # Handle metadata
        non_metadata_keys = {'fields', 'headers', 'beacons', 'messages'}
        pass_.metadata = {}
        for key in data.keys():
            if key not in non_metadata_keys:
                pass_.metadata[key] = data.pop(key)

        if pass_.metadata.get('templateId'):
            pass_.metadata[PassMetadata.TEMPLATE_ID] = pass_.metadata['templateId']
            del pass_.metadata['templateId']
        if pass_.metadata.get('id'):
            pass_.metadata[PassMetadata.PASS_ID] = pass_.metadata['id']
            del pass_.metadata['id']

        # Handle headers
        pass_.headers = data.pop('headers', {})
        if pass_.headers.get(ua.TemplateHeader.BARCODE_TYPE):
            no_pk = pass_.headers[ua.TemplateHeader.BARCODE_TYPE]['value'].replace('PKB', 'B')
            pass_.headers[ua.TemplateHeader.BARCODE_TYPE]['value'] = no_pk

        return pass_

    def view(self):
        payload = super(Pass, self)._create_payload()
        payload['fields'] = {}
        for name, field in self.fields.iteritems():
            payload['fields'][name] = field.build_pass_json()
        for name, item in self.metadata.iteritems():
            payload[name] = item
        return {key: val for key, val in payload.iteritems() if val}

    def _create_payload(self):
        payload = self.view()
        payload.get('publicUrl', {}).pop('path', None)
        payload.get('publicUrl', {}).pop('image', None)
        return {key: val for key, val in payload.iteritems() if
                key not in self.READ_ONLY_METADATA}

    def _add_metadata_helper(self, name, value):
        # publicUrl metadata is handled differently from other metadata keys
        if name == PassMetadata.PUBLIC_URL:
            self.set_public_url(value)
        else:
            super(Pass, self)._add_metadata_helper(name, value)

    # Additional convenience methods
    def set_expiration(self, date):
        """Set the pass expiration date.

        Arguments:
            date (datetime): A python datetime object.

        Example:
            >>> my_pass.set_expiration(datetime.datetime(2016,10,13))
        """
        # Implementation differs between apple/google. See overrides for
        # details.
        raise NotImplementedError

    def set_public_url(self, type_):
        """Set the public URL type.

        Arguments:
            type_ (string): A string representing the public URL type. Can be one of
                "single" or "multiple".

        Raises:
            ValueError: If ``type_`` is not one of "single" or "multiple".

        Example:
            >>> my_pass.set_public_url('single')
        """
        if type_ not in {'single', 'multiple'}:
            raise ValueError(
                "Unrecognized publicUrl type '{}'. Please use one of 'single' "
                "or 'multiple'.".format(type_)
            )
        self.metadata['publicUrl'] = {'type': type_}

    @staticmethod
    def build_url(
        base_url,
        main_id=None,
        template_external_id=None,
        pass_external_id=None,
        location_id=None
    ):
        if base_url == common.PASS_ADD_LOCATION_URL and main_id:
            return base_url.format(main_id)
        elif base_url == common.PASS_ADD_LOCATION_URL:
            return base_url.format('id/' + str(pass_external_id))
        elif base_url == common.PASS_DELETE_LOCATION_URL and main_id:
            return base_url.format(main_id, location_id)
        elif base_url == common.PASS_DELETE_LOCATION_URL:
            return base_url.format('id/' + str(pass_external_id), location_id)
        elif main_id and not (template_external_id or pass_external_id):
            return base_url.format(main_id)
        elif template_external_id and not (main_id or pass_external_id):
            return base_url.format('id/' + str(external_id))
        elif pass_external_id and main_id and not template_external_id:
            return base_url.format(str(main_id) + '/id/' + str(pass_external_id))
        elif template_external_id and pass_external_id and not main_id:
            return base_url.format(
                'id/' + str(template_external_id) + '/id/' + str(pass_external_id)
            )
        else:
            return base_url.format('')

    def __repr__(self):
        """Note: Cannot gaurantee that any displayable attributes will be
        present, so we revert back to the default __repr__ implementation.
        """
        return '<{}.{} object at {}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )


@util.inherit_docs
class ApplePass(Pass):

    def __init__(self):
        super(ApplePass, self).__init__()
        self._apple_features = ua.AppleTemplate()

    @classmethod
    def from_data(cls, data):
        pass_ = super(ApplePass, cls).from_data(data)
        pass_._apple_features.beacons = data.pop('beacons', [])
        fields = data.pop('fields', {})
        for name, json_field in fields.iteritems():
            pass_.fields[name] = ua.Field.build_apple_field(
                name, json_field
            )
        return pass_

    def view(self):
        payload = super(ApplePass, self).view()
        payload['beacons'] = self._apple_features.beacons
        payload.update(self.metadata)
        return {key: val for key, val in payload.iteritems() if val}

    def set_expiration(self, date):
        date_str = date.strftime('%Y-%m-%dT%H:%M')
        self.headers['expirationDate'] = {'value': date_str}

    @util.set_docstring(ua.AppleTemplate.add_beacon)
    def add_beacon(self, uuid, relevant_text=None, major=None, minor=None):
        self._apple_features.add_beacon(uuid, relevant_text, major, minor)

    @util.set_docstring(ua.AppleTemplate.remove_beacon)
    def remove_beacon(self, uuid):
        self._apple_features.remove_beacon(uuid)

    @util.set_docstring(ua.AppleTemplate.set_logo_image)
    def set_logo_image(self, value):
        self.add_headers(logo_image=value)


@util.inherit_docs
class GooglePass(Pass):

    def __init__(self):
        super(GooglePass, self).__init__()
        self._google_features = ua.GoogleTemplate()

    @classmethod
    def from_data(cls, data):
        pass_ = super(GooglePass, cls).from_data(data)
        for name, field in data.pop('fields', {}).iteritems():
            if name == 'image':
                pass_._google_features.top_level_fields['image'] = field
            elif name == ua.GoogleFieldType._IMAGE_MODULE:
                pass_._google_features.add_top_level_fields(
                    ua.GoogleFieldType._IMAGE_MODULE,
                    **field
                )
            elif name == ua.GoogleFieldType._MESSAGE_MODULE:
                pass_._google_features.messages = field
            elif name == ua.GoogleFieldType._OFFER_MODULE:
                pass_._google_features.add_top_level_fields(
                    ua.GoogleFieldType._OFFER_MODULE,
                    **field
                )
            else:
                pass_.fields[name] = ua.Field.build_google_field(name, field)
        return pass_

    def view(self):
        payload = super(GooglePass, self).view()
        if self._google_features.top_level_fields:
            payload['top_level_fields'] = self._google_features.top_level_fields
        if self._google_features.messages:
            payload['messages'] = self._google_features.messages
        return payload

    def _create_payload(self):
        payload = super(GooglePass, self)._create_payload()
        if payload.get('top_level_fields'):
            additional_fields = payload.pop('top_level_fields')
            if not payload.get('fields'):
                payload['fields'] = {}
            payload['fields'].update(additional_fields)
        return payload

    def set_expiration(self, date):
        date_str = date.strftime('%Y-%m-%dT%H:%M')
        self._google_features.top_level_fields['endTime'] = {'value': date_str}

    # Google-specific methods
    @util.set_docstring(ua.GoogleTemplate.set_logo_image)
    def set_logo_image(self, value, description=None):
        if not description:
            description = ''

        self._google_features.top_level_fields['image'] = {
            'title.string': value,
            'description.string': description
        }

    @util.set_docstring(ua.GoogleTemplate.set_background_image)
    def set_background_image(self, value, description=None):
        self._google_features.set_background_image(value, description)

    @util.set_docstring(ua.GoogleTemplate.set_offer)
    def set_offer(
        self,
        multi_user_offer=None,
        endtime=None,
        provider=None,
        redemption_channel=None
    ):
        self._google_features.set_offer(
            multi_user_offer, endtime, provider, redemption_channel
        )

    @util.set_docstring(ua.GoogleTemplate.add_message)
    def add_message(
        self,
        body=None,
        header=None,
        action_uri=None,
        action_uri_description=None,
        image_uri=None,
        image_description=None,
        starttime=None,
        endtime=None
    ):
        self._google_features.add_message(
            body,
            header,
            action_uri,
            action_uri_description,
            image_uri,
            image_description,
            starttime,
            endtime
        )
