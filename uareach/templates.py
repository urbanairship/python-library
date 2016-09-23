import json
import logging
from collections import defaultdict

import common
import uareach.fields as wf
from uareach import util


logger = logging.getLogger(__name__)


class TemplateMetadata(util.Constant):
    KEY_CLASS = 'TemplateMetadata'

    VENDOR = 'vendor'
    PROJECT_TYPE = 'project_type'
    TEMPLATE_TYPE = 'template_type'
    VENDOR_ID = 'vendorId'
    DELETED = 'deleted'
    DESCRIPTION = 'description'
    NAME = 'name'
    DISABLED = 'disabled'
    TEMPLATE_ID = 'template_id'
    PROJECT_ID = 'project_id'
    TYPE = 'type_'


class ProjectType(util.Constant):
    """Class representing possible projectTypes."""
    BOARDING_PASS = 'boardingPass'
    COUPON = 'coupon'
    EVENT_TICKET = 'eventTicket'
    GENERIC = 'generic'
    LOYALTY = 'loyalty'
    GIFT_CARD = 'giftCard'
    MEMBER_CARD = 'memberCard'


class TemplateType(util.Constant):
    """Class representing possible template types."""
    BOARDING_PASS = 'Boarding Pass'
    COUPON = 'Coupon'
    EVENT_TICKET = 'Event Ticket'
    GENERIC = 'Generic'
    STORE_CARD = 'Store Card'
    LOYALTY = 'Loyalty'
    OFFER = 'Offer'
    GIFT_CARD = 'Gift Card'


class Type(util.Constant):
    """These are template type, project type combinations that
    are known to work.

    .. note::

        There are currently discrepencies between Apple's and
        Google's acceptable (template)type and projectType
        pairs. These tuples represent Apple's pairing. For google,
        the _create_payload function under GoogleTemplate will perform
        the necessary conversions, ensuring the projectType and type
        keys are valid. In other words, these can be used for either
        Apple or Google templates.
    """
    LOYALTY = (TemplateType.STORE_CARD, ProjectType.LOYALTY)
    COUPON = (TemplateType.COUPON, ProjectType.COUPON)
    GIFT_CARD = (TemplateType.STORE_CARD, ProjectType.GIFT_CARD)
    MEMBER_CARD = (TemplateType.GENERIC, ProjectType.MEMBER_CARD)
    EVENT_TICKET = (TemplateType.EVENT_TICKET, ProjectType.EVENT_TICKET)
    BOARDING_PASS = (TemplateType.BOARDING_PASS, ProjectType.BOARDING_PASS)
    GENERIC = (TemplateType.GENERIC, ProjectType.GENERIC)


class TemplateHeader(util.Constant):
    KEY_CLASS = 'TemplateHeader'

    BACKGROUND_COLOR = 'background_color'
    BACKGROUND_IMAGE = 'background_image'
    BARCODE_ALT_TEXT = 'barcodeAltText'
    BARCODE_ENCODING = 'barcode_encoding'
    BARCODE_TYPE = 'barcode_type'
    BARCODE_VALUE = 'barcode_value'
    EXPIRATION_DATE = 'expirationDate'
    FOOTER_IMAGE = 'footer_image'
    FOREGROUND_COLOR = 'foreground_color'
    ICON_IMAGE = 'icon_image'
    LOGO_COLOR = 'logo_color'
    LOGO_IMAGE = 'logo_image'
    LOGO_TEXT = 'logo_text'
    STRIP_IMAGE = 'strip_image'
    SUPPRESS_STRIP_SHINE = 'suppress_strip_shine'
    THUMBNAIL_IMAGE = 'thumbnail_image'
    TRANSIT_TYPE = 'transitType'

    @classmethod
    def google_headers(cls):
        return [
            cls.BARCODE_ALT_TEXT,
            cls.BARCODE_TYPE,
            cls.BARCODE_ENCODING,
            cls.BARCODE_VALUE,
            cls.STRIP_IMAGE,
            cls.SUPPRESS_STRIP_SHINE,
            cls.EXPIRATION_DATE,
        ]


class BarcodeType(util.Constant):
    PDF_417 = 'PDF_417'
    AZTEC = 'AZTEC'
    QR_CODE = 'QR_CODE'
    CODE_128 = 'CODE_128'
    UPC_A = 'UPC_A'
    EAN_13 = 'EAN_13'
    CODE_39 = 'CODE_39'

    @classmethod
    def convert_to_apple(cls, value):
        if value == cls.PDF_417:
            return 'PKBarcodeFormatPDF417'
        elif value == cls.AZTEC:
            return 'PKBarcodeFormatAztec'
        elif value == cls.QR_CODE:
            return 'PKBarcodeFormatQR'
        elif value == cls.CODE_128:
            return 'PKBarcodeFormatCode128'
        else:
            raise ValueError("Invalid Apple barcode_type '{}'".format(value))


class TransitType(util.Constant):
    GENERIC = 'transitTypeGeneric'
    BUS = 'transitTypeBus'
    AIR = 'transitTypeAir'
    BOAT = 'transitTypeBoat'
    TRAIN = 'transitTypeTrain'


def get_template(reach, template_id=None, external_id=None):
    """Retrieve a template.

    Arguments:
        reach (reach.core.Reach): A uareach client object.
        template_id (str or int): The template ID of the template you wish
            to delete.
        external_id (str or int): The external ID of the template you wish
            to delete.

    Returns:
        An AppleTemplate or GoogleTemplate object.

    Raises:
        ValueError: If neither, or both, of template_id and external_id
            is specified.

    Example:
        >>> my_template = get_template(external_id=12345)
        <Template name:SummerSale, vendor:Apple>
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = reach.request(
        method='GET',
        body=None,
        url=Template.build_url(
            common.TEMPLATE_BASE_URL,
            main_id=template_id,
            external_id=external_id
        ),
        version=1.2
    )
    payload = response.json()
    logger.info('Successfully retrieved template: {}.'.format(
        template_id if template_id else external_id
    ))
    return _template_create_dispatch(payload)


def _template_create_dispatch(data):
    """Helper function, called by get_template. Determines whether
    the retrieved template is Apple or Google.

    Arguments:
        data (dict): A dictionary to be loaded into an AppleTemplate or
            GoogleTemplate object.
    Raises:
        ValueError: If the template vendor is not 'Apple' or 'Google'.
        KeyError: If the json template structure is unrecognized.
    Returns:
        An Apple or Google template.
    Example:
        >>> template_create_dispatch(template_dictionary)
        <Template name:SummerSale, vendor:Apple>
    """
    try:
        vendor = data['templateHeader']['vendor']
        if vendor == 'Apple':
            return AppleTemplate.from_data(data)
        elif vendor == 'Google':
            return GoogleTemplate.from_data(data)
        else:
            raise ValueError('Unrecognized vendor: {}'.format(vendor))
    except KeyError as k:
        logger.exception('Unrecognized template structure: {}'.format(data))
        raise


def delete_template(reach, template_id=None, external_id=None):
    """Delete a template.

    Arguments:
        reach (reach.core.Reach): A UA Reach object.
        template_id (str or int): The ID of the template you wish to delete.
        external_id (str or int): The external ID of the template you wish
            to delete.

    Returns:
        A boolean representing success.

    Raises:
        ValueError: If neither, or both, of template_id and external_id
            are specified.

    Example:
        >>> delete_template(ua_reach, template_id=123456)
        True
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = reach.request(
        method='DELETE',
        body=None,
        url=Template.build_url(
            common.TEMPLATE_BASE_URL,
            main_id=template_id,
            external_id=external_id
        ),
        version=1.2
    )
    logger.info('Successful template deletion: {}'.format(
        template_id if template_id else external_id
    ))
    return True


def duplicate_template(reach, template_id=None, external_id=None):
    """Duplicate a template.

    Arguments:
        reach (reach.core.Reach): A UA Reach object.
        template_id (str or int): The ID of the template you wish to delete.
        external_id (str or int): The external ID of the template you wish
            to delete.

    Returns:
        A dictionary containing the id of the newly created template.

    Raises:
        ValueError: If neither, or both, of template_id and external_id
            are specified.

    Example:
        >>> duplicate_template(ua_reach, template_id=12345)
        {'templateId': 12346}
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = reach.request(
        method='POST',
        body=None,
        url=Template.build_url(
            common.TEMPLATE_DUPLICATE_URL,
            main_id=template_id,
            external_id=external_id
        ),
        version=1.2
    )
    logger.info('Successfully created template copy: {}'.format(
        template_id if template_id else external_id
    ))
    return response.json()


def add_template_locations(
    reach, locations, template_id=None, external_id=None
):
    """Add locations to a template.

    Arguments:
        reach (reach.core.Reach): A uareach client object.
        locations (list of dicts): A list of location objects, represented
            as dictionaries.
        template_id (str or int): The ID of the template you wish to add
            locations to.
        external_id (str or int): The external ID of the template you wish to add
            locations to.

    Returns:
        A list of dicts, each containing the location value, locationId,
            and fieldId.

    Raises:
        ValueError: If neither, or both of, template_id and external_id
            are specified.

    Example:
        >>> add_template_locations(
        ...     ua_reach, [location1, location2], template_id=12345
        ... )
        [{'value': { '...' }, 'locationId': 12345, 'fieldId': 54321},
         {'value': { '...' }, 'locationId': 56789, 'fieldId': 98765}]
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = reach.request(
        method='POST',
        body=json.dumps({'locations': locations}),
        url=Template.build_url(
            common.TEMPLATE_ADD_LOCATION_URL,
            main_id=template_id,
            external_id=external_id
        ),
        content_type='application/json',
        version=1.2
    )
    logger.info("Successfully added {} locations to template '{}'.".format(
        len(locations),
        template_id if template_id else external_id
    ))
    return response.json()


def delete_template_location(
        reach, location_id, template_id=None, external_id=None
):
    """Remove a location from a template

    Arguments:
        reach (reach.core.Reach): A uareach client object.
        location_id (str or int): The ID of the location you wish to remove.
        template_id (str or int): The ID of the template you wish to remove
            locations from.
        external_id (str or int): The external ID of the template you wish
            to remove locations from.

    Returns:
        A boolean representing success.

    Raises:
        ValueError: If both or neither of template_id and external_id are
            specified.

    Example:
        >>> delete_template_location(ua_reach, 12345, template_id=44444)
        True
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = reach.request(
        method='DELETE',
        body=None,
        url=Template.build_url(
            common.TEMPLATE_REMOVE_LOCATION_URL,
            main_id=template_id,
            external_id=external_id,
            location_id=location_id
        ),
        version=1.2
    )
    logger.info("Successfully removed location '{}' from template '{}'.".format(
        location_id,
        template_id if template_id else external_id
    ))

    return True


class TemplateList(common.IteratorParent):
    """Forms a template listing request.

    Arguments:
        reach (reach.core.Reach): The uareach client object.
        page_size (int): The size of each page of the template listing
            response. Defaults to 10.
        page (int): The page to start the listing response on. Defaults
            to 1.
        order (string): The attribute used to order the templates. Can be one
            of ``"id"``, ``"name"``, ``"createdAt"``, or ``"updatedAt"``.
            Defaults to ``"id"``.
        direction (string): The direction of the template list, can be one of
            ``"ASC"`` or ``"DESC"``. Defaults to ``"DESC"``.

    Example:
        >>> template_list = TemplateList()
        >>> for item in template_list:
        ...     print item['createdAt']
        ...
        2016-07-27T21:14:47Z
        2016-07-23T12:13:32Z
        2016-06-09T17:32:14Z

    """
    base_url = common.TEMPLATE_BASE_URL.format('headers')
    data_attribute = 'templateHeaders'

    def __init__(
            self, reach, page_size=None, page=None, order=None, direction=None
    ):
        if direction not in {None, 'ASC', 'DESC'}:
            raise ValueError(
                'Unrecognized direction "{}". '
                'Please use one of "ASC" or "DESC"'.format(direction)
            )

        params = {
            'pageSize': page_size,
            'page': page,
            'order': order,
            'direction': direction
        }
        params = {k: v for k, v in params.iteritems() if v is not None}
        super(TemplateList, self).__init__(reach, params)


class Template(object):
    """Superclass for representing a uareach Template class. Should not be used
    directly -- use AppleTemplate or GoogleTemplate to perform template
    operations.
    """
    HEADERS = TemplateHeader
    HEADER_MAP = {
        TemplateHeader.BACKGROUND_COLOR:     {'fieldType': 'topLevel', 'formatType': 'String'},
        TemplateHeader.BACKGROUND_IMAGE:     {'fieldType': 'image', 'formatType': 'String'},
        TemplateHeader.BARCODE_ALT_TEXT:     {'fieldType': 'barcode', 'formatType': 'String'},
        TemplateHeader.BARCODE_ENCODING:     {'fieldType': 'barcode', 'formatType': 'String'},
        TemplateHeader.BARCODE_TYPE:         {'fieldType': 'barcode', 'formatType': 'String'},
        TemplateHeader.BARCODE_VALUE:        {'fieldType': 'barcode', 'formatType': 'String'},
        TemplateHeader.EXPIRATION_DATE:      {'fieldType': 'topLevel', 'formatType': 'String'},
        TemplateHeader.FOOTER_IMAGE:         {'fieldType': 'image', 'formatType': 'String'},
        TemplateHeader.FOREGROUND_COLOR:     {'fieldType': 'topLevel', 'formatType': 'String'},
        TemplateHeader.ICON_IMAGE:           {'fieldType': 'image', 'formatType': 'String'},
        TemplateHeader.LOGO_COLOR:           {'fieldType': 'topLevel', 'formatType': 'String'},
        TemplateHeader.LOGO_IMAGE:           {'fieldType': 'image', 'formatType': 'String'},
        TemplateHeader.LOGO_TEXT:            {'fieldType': 'topLevel', 'formatType': 'String'},
        TemplateHeader.STRIP_IMAGE:          {'fieldType': 'image', 'formatType': 'String'},
        TemplateHeader.SUPPRESS_STRIP_SHINE: {'fieldType': 'topLevel', 'formatType': 'String'},
        TemplateHeader.THUMBNAIL_IMAGE:      {'fieldType': 'image', 'formatType': 'String'},
        TemplateHeader.TRANSIT_TYPE:         {'fieldType': 'passTop', 'formatType': 'String'},
    }

    METADATA = TemplateMetadata
    READ_ONLY_METADATA = ['createdAt', 'template_id', 'updatedAt', 'project_id']

    def __init__(self):
        self.headers = {}
        self.fields = defaultdict(dict)
        self.metadata = {}

    def create(self, reach, project_id=None, external_id=None):
        """Submits a template create request to the API.

        Arguments:
            reach (reach.core.Reach): A uareach client object.
            project_id (str or int): A project ID.
            external_id (str or int): An external ID.

        Returns:
            A dict containing the template ID.

        Example:
            >>> template.create_template(ua_reach, project_id=12345)
            {'templateId': 54321}
        """
        if not project_id:
            try:
                project_id = self.metadata[TemplateMetadata.PROJECT_ID]
            except KeyError:
                raise ValueError(
                    "Either set project_id when calling update, "
                    "or set the project_id attribute via the add_metadata "
                    "method, e.g., your_template.add_metadata(project_id=1234)."
                )

        payload = self._create_payload()
        self._validate(payload)
        response = reach.request(
            method='POST',
            body=json.dumps(payload),
            url=Template.build_url(
                common.TEMPLATE_BASE_URL,
                main_id=project_id,
                external_id=external_id
            ),
            content_type='application/json',
            version=1.2
        )
        template_id = response.json().get('templateId')
        logger.info('Successful template creation -- ID: {}, EXTERNAL_ID: {}'.format(
            template_id, external_id
        ))
        self.metadata[TemplateMetadata.TEMPLATE_ID] = template_id
        return {'templateId': template_id}

    def update(self, reach, template_id=None, external_id=None):
        """Submits a template update request to the API.

        Arguments:
            reach (reach.core.Reach): A uareach client object.
            template_id (str or int): A template ID.
            external_id (str or int): An external ID.

        Returns:
            A boolean representing success.

        Example:
            >>> template.update(ua_reach)
            True
        """
        if template_id and external_id:
            raise ValueError('Only set one of template_id or external_id.')
        if not external_id and not template_id:
            try:
                template_id = self.metadata[TemplateMetadata.TEMPLATE_ID]
            except KeyError:
                raise ValueError(
                    "Either set template_id or external_id when calling "
                    "update, or set the template id attribute via the "
                    "add_metadata method, e.g., "
                    "your_template.add_metadata(template_id=1234)."
                )

        payload = self._create_payload()
        self._validate(payload)
        response = reach.request(
            method='PUT',
            body=json.dumps(payload),
            url=Template.build_url(
                common.TEMPLATE_BASE_URL,
                main_id=template_id,
                external_id=external_id
            ),
            content_type='application/json',
            version=1.2
        )
        logger.info('Successful template creation: {}'.format(
            template_id if template_id else external_id
        ))
        return True

    @classmethod
    def from_data(cls, data):
        """Create a template/pass from JSON data.

        Arguments:
            data (dict): The JSON data to convert to a template or pass
                object.

        Returns:
            An Apple or Google template object.

        Example:
            >>> loyalty_template = AppleTemplate.from_data({
            ...     'name': 'Loyalty Template',
            ...     'description': 'A loyalty template',
            ...     'fieldsModel': {
            ...         'fields': {
            ...             ...
            ...         },
            ...         'headers': {
            ...             ...
            ...         }
            ...     },
            ...     ...,
            ...     'vendor': 'Apple'
            ... })
            <Template name:Loyalty Template, vendor:Apple>
        """
        template = cls()
        # Handle Metadata
        template.metadata = data.get('templateHeader', {})
        # Convert id values to descriptive keys
        if template.metadata.get('id'):
            template.metadata[TemplateMetadata.TEMPLATE_ID] = template.metadata['id']
            del template.metadata['id']
        if template.metadata.get('projectId'):
            template.metadata[TemplateMetadata.PROJECT_ID] = template.metadata['projectId']
            del template.metadata['projectId']

        # Handle headers
        template.headers = data.get('fieldsModel', {}).pop('headers', {})
        if template.headers.get(TemplateHeader.BARCODE_TYPE):
            no_pk = template.headers[TemplateHeader.BARCODE_TYPE]['value'].replace('PKB', 'B')
            template.headers[TemplateHeader.BARCODE_TYPE]['value'] = no_pk

        # Handle user_locations
        if data.get('userlocations'):
            template.user_locations = data.pop('userlocations')
        return template

    """ Field manipulation """
    def add_fields(self, *args):
        """Add uareach.fields.Field objects.

        Arguments:
            args (reach.fields.Field): Field objects to add to your template or
                pass.

        Example:
            >>> points_field = Field(name='Rewards Points', fieldType='primary')
            >>> member_field = Field(name='Member Name', fieldType='secondary')
            >>> template_or_pass.add_fields(points_field, member_field)
        """
        for field in args:
            self.fields[field.name] = field

    def remove_fields(self, *args):
        """Removes uareach.fields.Field objects.

        Arguments:
            args (string): The names of the fields to be deleted, e.g.,
                'Rewards Points'/'Member Name'/'Background'

        Example:
            >>> template_or_pass.remove_fields('Rewards Points', 'Member Name')
        """
        for name in args:
            del self.fields[name]

    def set_fields(self, *args):
        """Set the uareach.fields.Field objects. Will overwrite any existing
        fields set on the template or pass.

        Arguments:
            *args (reach.fields.Field): Field objects to add to your template or
                pass.

        Example:
            >>> points_field = Field(name='Rewards Points', fieldType='primary')
            >>> member_field = Field(name='Member Name', fieldType='secondary')
            >>> template_or_pass.set_fields(points_field, member_field)
        """
        self.fields.clear()
        self.add_fields(*args)

    """ Metadata manipulation. """
    def add_metadata(self, **kwargs):
        """Add metadata items.

        .. note::

            If working with a template, acceptable keys are accessible through
            TemplateMetadata. Likewise, if working with a pass, acceptable keys
            are accessible through PassMetadata.

        Arguments:
            **kwargs: Key, value pairs specifying the metadata items to add.

        Example:
            >>> template.add_metadata(
            ...     project_type='memberCard',
            ...     template_type='Store Card',
            ...     description='Hello this is a description'
            ... )
            >>> # method is identical for passes, but acceptable keys differ
            >>> pass_.add_metadata(
            ...     pass_id=12345
            ... )
        """
        for header, value in kwargs.iteritems():
            self.METADATA.validate(header)
            self._add_metadata_helper(header, value)

    def remove_metadata(self, *args):
        """Remove metadata items

        .. note::

            If working with a template, acceptable strings are accessible through
            TemplateMetadata. Likewise, if working with a pass, acceptable strings
            are accessible through PassMetadata.

        Arguments:
            *args (strings): Keys of the metadata values to remove.

        Example:
            >>> my_template.remove_metadata('projectType', 'description')
            >>> my_pass.remove_metadata('pass_id')
        """
        for name in args:
            del self.metadata[name]

    def set_metadata(self, **kwargs):
        """Remove all currently set metadata items and then add the
        specified metadata

        .. note::

            If working with a template, acceptable keys are accessible through
            TemplateMetadata. Likewise, if working with a pass, acceptable keys
            are accessible through PassMetadata.

        Arguments:
            **kwargs: Key, value pairs specifying the metadata items to add.

        Example:
            >>> template.set_metadata(
            ...     project_type='memberCard',
            ...     template_type='Store Card',
            ...     description='Hello this is a description'
            ... )
            >>> # method is identical for passes, but acceptable keys differ
            >>> pass_.set_metadata(
            ...     pass_id=12345
            ... )
        """
        self.metadata.clear()
        self.add_metadata(**kwargs)

    def _add_metadata_helper(self, name, value):
        """Does validation on metadata (key, val) pairs, then set metadata
        if it passes validation.
        """
        self.METADATA.validate(name)
        if name == self.METADATA.TEMPLATE_TYPE:
            self.metadata['type'] = value
        elif name == self.METADATA.PROJECT_TYPE:
            self.metadata['projectType'] = value
        elif name == self.METADATA.TYPE:
            Type.validate(value)
            self.metadata['type'] = value[0]
            self.metadata['projectType'] = value[1]
        else:
            self.metadata[name] = value

    """ Header manipulation. """
    def add_header(self, header, value, format_type=None, field_type=None):
        """Add a header.

        Arguments:
            header (str): The header, represented as a string
                (e.g. 'logo_color')
            value (str): The header value.

        Raises:
            ValueError: If the `header` is not contained in Header.values

        Example:
            >>> template_or_pass.add_header('barcode_value', '123456789')
        """
        self.HEADERS.validate(header)
        if header == self.HEADERS.BARCODE_TYPE:
            BarcodeType.validate(value)

        # Use the default formatType and fieldType values if not specified.
        if format_type is None:
            format_type = self.HEADER_MAP[header]['formatType']
        if field_type is None:
            field_type = self.HEADER_MAP[header]['fieldType']

        self.headers[header] = {
            'formatType': format_type,
            'fieldType': field_type,
            'value': value
        }

    def add_headers(self, **kwargs):
        """Add multiple headers.

        Arguments:
            **kwargs: Key, value pairs specifying header values.

        Example:
            >>> template_or_pass.add_headers(
            ...     barcode_value='iso-8859-1',
            ...     logo_image='https://google.com/fun.png'
            ... )
        """
        for header, value in kwargs.iteritems():
            self.add_header(header, value)

    def remove_headers(self, *args):
        """Remove headers.

        Arguments:
            *args (list of strings): A list of header values to remove.

        Example:
            >>> template_or_pass.remove_headers('logo_color', 'icon_image')
        """
        for header in args:
            del self.headers[header]

    def set_headers(self, **kwargs):
        """Remove all currently set headers and then add the
        specified headers.

        Arguments:
            **kwargs: Header specifications. Note that the keywords must be one
                of the keys listed in Header.values

        Example:
            >>> template.set_headers(
            ...     barcode_value='iso-8859-1',
            ...     logo_image='https://google.com/fun.png'
            ... )
        """
        self.headers.clear()
        self.add_headers(**kwargs)

    def view(self):
        """View the entirety of the template or pass, including keys that
        are read-only.

        Returns:
            A dict representing the template or pass.

        Example:
            >>> my_template.view()
            {'headers': {...}, 'fields': {...}, 'key1': 'val1', ... }
        """
        payload = {'headers': self.headers}
        payload.update(self.metadata)
        return payload

    def _create_payload(self):
        """Formats the payload for a request. Filters out read-only items,
        and handles formatting differences between Apple and Google.
        """
        payload = {'headers': {}}
        for key, val in self.headers.iteritems():
            payload['headers'][key] = val
        for key, val in self.metadata.iteritems():
            if key not in self.READ_ONLY_METADATA:
                payload[key] = val
        return payload

    @staticmethod
    def _validate(payload):
        pass

    @staticmethod
    def build_url(url, main_id=None, external_id=None, location_id=None):
        if location_id and main_id:
            return url.format(main_id, location_id)
        elif location_id:
            return url.format('id/' + str(external_id), location_id)
        elif main_id and external_id:
            return url.format(str(main_id) + '/id/' + str(external_id))
        elif main_id:
            return url.format(main_id)
        else:
            return url.format('id/' + str(external_id))


@util.inherit_docs
class AppleTemplate(Template):
    """Represents an Apple template object."""

    def __init__(self):
        super(AppleTemplate, self).__init__()
        self.beacons = []
        self.metadata['vendor'] = 'Apple'
        self.metadata['vendorId'] = 1

    @classmethod
    def from_data(cls, data):
        template = super(AppleTemplate, cls).from_data(data)
        fields = data.get('fieldsModel', {}).get('fields', {})
        for name, json_field in fields.iteritems():
            template.fields[name] = wf.Field.build_apple_field(
                name, json_field
            )
        template.beacons = data.get('beacons', [])
        return template

    def view(self):
        payload = super(AppleTemplate, self).view()
        payload.update({'fields': {}, 'beacons': []})
        for name, field in self.fields.iteritems():
            field._build_common_template_json()
            payload['fields'][name] = field.build_apple_json()
        payload['beacons'] = self.beacons
        return payload

    def add_header(self, header, value, format_type=None, field_type=None):
        # Check Apple-specific enums
        if header == self.HEADERS.TRANSIT_TYPE:
            TransitType.validate(value)

        super(AppleTemplate, self).add_header(
            header, value, format_type, field_type
        )

        # Apple-specific validation
        if header == TemplateHeader.BARCODE_TYPE:
            try:
                self.headers[header]['value'] = BarcodeType.convert_to_apple(value)
            except ValueError:
                del self.headers[header]
                raise

    def _create_payload(self):
        payload = self.view()
        return {key: val for key, val in payload.iteritems() if
                key not in self.READ_ONLY_METADATA}

    def set_logo_image(self, value):
        """Set the logo image.

        Notes:
            This is mainly here to provide parity with the GoogleTemplate
            class. You could equivalently do template_or_pass.set_headers(logo_image='image')

        Arguments:
            value (str): A URL path to an image.

        Example:
            >>> template_or_pass.set_logo_image('https://urbanairship.com/cool_image.png')
        """
        self.set_headers(logo_image=value)

    # Apple-specific methods
    def add_beacon(self, uuid, relevant_text=None, major=None, minor=None):
        """Add a beacon to the template.

        Arguments:
            uuid (str): An identifier for this location.
            relevant_text (str): Text to display when a user approaches the
                location.
            major (int): A major location identifier.
            minor (int): A minor location identifier.

        Example:
            >>> template.add_beacon(
            ...     uuid='3526dee6-4ea8-11e6-beb8-9e71128cae77',
            ...     relevant_text='You are near something cool.',
            ...     major=2,
            ...     minor=34
            ... )
        """
        payload = {
            'uuid': uuid,
            'relevantText': relevant_text,
            'major': major,
            'minor': minor
        }

        self.beacons.append({
            key: val for key, val in payload.iteritems() if val is not None
        })

    def remove_beacon(self, uuid):
        """Remove a beacon from a template.

        Arguments:
            uuid (str): The UUID of the beacon you wish to remove.

        Raises:
            ValueError: When the uuid does not match any beacon associated
                with the template

        Example:
            >>> template.remove_beacon('8054f07e-238f-439e-93eb-0c2fe6829541')
        """
        for index, beacon in enumerate(self.beacons):
            if beacon['uuid'] == uuid:
                del self.beacons[index]
                return
        raise ValueError("Beacon with UUID {} not found".format(uuid))


@util.inherit_docs
class GoogleTemplate(Template):
    """Represents a Google template object."""

    # Some modules have reserved names (names that have special meaning and
    # cannot be used for field names).
    RESERVED_NAMES = {
        wf.GoogleFieldType.INFO_MODULE: ['hexFontColor', 'hexBackgroundColor'],
        wf.GoogleFieldType.TITLE_MODULE: ['image'],
        wf.GoogleFieldType._IMAGE_MODULE: ['imageModulesData']
    }

    def __init__(self):
        super(GoogleTemplate, self).__init__()
        self.top_level_fields = defaultdict(dict)
        self.messages = []
        self.metadata['vendor'] = 'Google'
        self.metadata['vendorId'] = 2

    # Override methods
    @classmethod
    def from_data(cls, data):
        template = super(GoogleTemplate, cls).from_data(data)
        modules = data.get('fieldsModel', {})
        for field_type, module_data in modules.iteritems():
            if field_type == 'vendor':
                continue
            # Handling special modules
            elif field_type == wf.GoogleFieldType._OFFER_MODULE:
                template.add_top_level_fields(
                    wf.GoogleFieldType._OFFER_MODULE,
                    **module_data
                )
            elif field_type == wf.GoogleFieldType._MESSAGE_MODULE:
                template.messages = module_data
            elif field_type == wf.GoogleFieldType._IMAGE_MODULE:
                if module_data.get(wf.GoogleFieldType._IMAGE_MODULE):
                    inner_module = module_data[wf.GoogleFieldType._IMAGE_MODULE]
                    template.add_top_level_fields(
                        wf.GoogleFieldType._IMAGE_MODULE,
                        **inner_module
                    )
            else:
                template._process_module_data(field_type, module_data)
        return template

    def view(self):
        payload = super(GoogleTemplate, self).view()
        payload.update({'fields': {}, 'messages': []})
        for name, field in self.fields.iteritems():
            field._build_common_template_json()
            payload['fields'][name] = field.build_google_template_json()
        payload['top_level_fields'] = self.top_level_fields
        payload['messages'] = self.messages
        return payload

    def _create_payload(self):
        payload = super(GoogleTemplate, self)._create_payload()

        # Handle type conversions
        if payload['projectType'] == ProjectType.COUPON:
            payload['type'] = TemplateType.OFFER
        if payload['projectType'] == ProjectType.GIFT_CARD:
            payload['type'] = TemplateType.GIFT_CARD
        if payload['projectType'] == ProjectType.LOYALTY:
            payload['type'] = TemplateType.LOYALTY

        # Handle standard fields
        for name, field in self.fields.iteritems():
            if not payload.get(field['fieldType']):
                payload[field['fieldType']] = {}
            field._build_common_template_json()
            payload[field['fieldType']][field.name] = field.build_google_template_json()

        # Handle top-level fields
        for field_type, fields in self.top_level_fields.iteritems():
            if not payload.get(field_type):
                payload[field_type] = {}
            payload[field_type].update(fields)

        # Handle messages
        if self.messages:
            payload['messages'] = self.messages

        return payload

    def add_header(self, header, value, format_type=None, field_type=None):
        super(GoogleTemplate, self).add_header(
            header, value, format_type, field_type
        )

        if header not in self.HEADERS.google_headers():
            del self.headers[header]
            raise ValueError(
                "The header '{}' is not used with "
                "Google templates".format(header)
            )

    def set_logo_image(self, value, description=None):
        """Set the logo image.

        Arguments:
            value (string): A URL pointing to an image.
            description (string): An optional string describing the logo
                image.

        Example:
            >>> template.set_logo_image(
            ...     'https://imgur.com/cool_image.png',
            ...     description='A super cool image'
            ... )
        """
        if not description:
            description = ''

        self.add_top_level_fields(
            wf.GoogleFieldType.TITLE_MODULE,
            image=value,
            imageDescription=description
        )

    def set_background_image(self, value, description=None):
        """Set the background image.

        Arguments:
            value (string): A URL pointing to an image.
            description (string): An optional string describing the background
                image.

        Example:
            >>> template.set_background_image(
            ...     'https://imgur.com/cool_image.png',
            ...     description='A super cool image'
            ... )
        """
        if not description:
            description = ''

        self.add_top_level_fields(
            wf.GoogleFieldType._IMAGE_MODULE,
            **{'image': value, 'imageDescription': description}
        )

    # Google-specific methods
    def add_top_level_fields(self, field_type, **kwargs):
        """Add top level values to the specified module location.

        Arguments:
            location (str): The module being added to.
            **kwargs: A mapping of string keys to string values.

        Raises:
            ValueError: If the location is not specified

        Example:
            >>> template.add_top_level_fields(
            ...     GoogleFieldType.TITLE_MODULE,
            ...     image="https://google.com/images/asdfoi1.png",
            ...     imageDescription="Logo Image"
            ... )

        """
        wf.GoogleFieldType.validate(field_type, allow_private=True)
        for key, val in kwargs.iteritems():
            self.top_level_fields[field_type][key] = val

    def set_offer(
        self,
        multi_user_offer=None,
        endtime=None,
        provider=None,
        redemption_channel=None
    ):
        """Set the offerModule.

        Arguments:
            * multi_user_offer (bool): One of True or False. Indicates
              whether the offer can be used by multiple users.
            * endtime (datetime.datetime): The offer expiration date.
            * provider (string): The provider name of the offer.
            * redemption_channel (string): Can be one of ``'online'``,
              ``'instore'``, ``'both'``, or ``'temporaryPriceReduction'``.

        Example:
            >>> template.set_offer(
            ...     multi_user_offer=False,
            ...     provider='UA'
            ...     redemption_channel='both',
            ... )
        """
        valid_chans = {'instore', 'online', 'both', 'temporaryPriceReduction'}
        if redemption_channel and redemption_channel not in valid_chans:
            raise ValueError(
                "Unrecognized redemption_channel '{}'. Valid \
                redemption_channels are: {}.".format(
                    redemption_channel, ', '.join(valid_chans)
                )
            )

        payload = {
            'multiUserOffer': multi_user_offer,
            'endTime': endtime.strftime('%Y-%m-%dT%H:%M') if endtime else None,
            'provider': provider,
            'redemptionChannel': redemption_channel
        }
        self.add_top_level_fields(
            wf.GoogleFieldType._OFFER_MODULE,
            **{key: val for key, val in payload.iteritems() if val != None}
        )

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
        """Add a message object.

        Arguments:
            * body (string): The message body.
            * header (string): The message header.
            * action_uri (string): The URI to which users are directed
              upon clicking the message.
            * action_uri_description (string): Description for the
              ``action_uri``.
            * image_uri (string): Specify an image to display with the
              message.
            * image_description (string): Description for the image.
            * starttime (datetime.datetime): Valid ISO8805 date for start
              time of a message.
            * endtime (datetime.datetime): Valid ISO8805 date for end time of
              a message.

        Example:
            >>> template.add_message(
            ...     body='A message body',
            ...     header='A message header'
            ... )
        """
        if not body:
            raise ValueError("The 'body' key must be specified for each message.")

        payload = {
            'body': body,
            'header': header,
            'actionUri': action_uri,
            'actionUriDescription': action_uri_description,
            'imageUri': image_uri,
            'imageDescription': image_description,
            'startTime': starttime.strftime('%Y-%m-%dT%H:%M') if starttime else None,
            'endTime': endtime.strftime('%Y-%m-%dT%H:%M') if endtime else None
        }
        self.messages.append(
            {key: val for key, val in payload.iteritems() if val != None}
        )

    def _process_module_data(self, field_type, module_data):
        """Handle each module (e.g. textModulesData, etc).
        """
        for name, data in module_data.iteritems():
            if name in GoogleTemplate.RESERVED_NAMES.get(field_type, []):
                self._handle_reserved_names(field_type, name, data)
            elif isinstance(data, dict):
                self.fields[name] = wf.Field.build_google_field(name, data)
            elif isinstance(data, str):
                self.add_top_level_field(field_type, name, data)
            else:
                ValueError('Unrecognized Android template structure.')

    def _handle_reserved_names(self, field_type, name, data):
        """Handles specialized module data.
        """
        value = data.get(wf.Field.GOOGLE_VALUE_MAP[field_type])
        if name == 'hexFontColor':
            self.add_top_level_field(field_type, hexFontColor=value)
        elif name == 'hexBackgroundColor':
            self.add_top_level_field(field_type, hexBackgroundColor=value)
        elif name == 'image':
            self.add_top_level_fields(field_type, image=data['title.string'])
            if 'description.string' in data:
                self.add_top_level_fields(
                    field_type, imageDescription=data['description.string']
                )
        else:
            raise ValueError('Unrecognized reserved name: {}'.format(name))

    @staticmethod
    def _validate_payload(payload):
        """Validates the structure of a Google Template.
        """
        if not payload.get(ua.GoogleFieldType.TITLE_MODULE):
            raise ValueError('Must add a title field to the template.')
        if not payload.get(ua.GoogleFieldType.TITLE_MODULE, {}).get('image'):
            raise ValueError("Must use set_logo_image to set your template's logo image.")
