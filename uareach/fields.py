import collections
import copy
import datetime
import logging

from six.moves.urllib import parse

from uareach import util


logger = logging.getLogger(__name__)

class FieldKey(util.Constant):
    KEY_CLASS = 'Field'

    CHANGE_MESSAGE = 'changeMessage'
    FORMAT_TYPE = 'formatType'
    HIDE_EMPTY = 'hideEmpty'
    ORDER = 'order'
    REQUIRED = 'required'
    FIELD_TYPE = 'fieldType'
    CURRENCY_CODE = 'currencyCode'
    TEXT_ALIGNMENT = 'textAlignment'
    LABEL = 'label'
    VALUE = 'value'

    # Specific to Google
    COL = 'col'
    ROW = 'row'

    # Specific to Apple
    NUMBER_STYLE = 'numberStyle'


class GoogleFieldType(util.Constant):
    INFO_MODULE = 'infoModuleData'
    TEXT_MODULE = 'textModulesData'
    LINKS_MODULE = 'linksModuleData'
    POINTS_MODULE = 'pointsModule'
    NOT_ASSIGNED = 'notAssigned'
    TITLE_MODULE = 'titleModule'
    ACCOUNT_MODULE = 'acctModule'

    _LOYALTY_POINTS = 'loyaltyPoints'
    _OFFER_MODULE = 'offerModule'
    _IMAGE_MODULE = 'imageModulesData'
    _MESSAGE_MODULE = 'messageModule'


class AppleFieldType(util.Constant):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    TERTIARY = 'tertiary'
    AUXILIARY = 'auxiliary'
    BACK = 'back'
    HEADER = 'header'
    NOT_ASSIGNED = 'notAssigned'


class TextAlignment(util.Constant):
    LEFT = 'textAlignmentLeft'
    CENTER = 'textAlignmentCenter'
    RIGHT = 'textAlignmentRight'
    NATURAL = 'textAlignmentNatural'


class NumberStyle(util.Constant):
    DECIMAL = 'numberStyleDecimal'
    TEXT = 'numberStyleSpellOut'
    SCIENTIFIC = 'numberStyleScientific'
    PERCENT = 'numberStylePercent'


class CurrencyCode(util.Constant):
    USD = 'USD'
    EUR = 'EUR'
    CNY = 'CNY'
    JPY = 'JPY'
    GBP = 'GBP'
    RUB = 'RUB'
    AUD = 'AUD'
    CHF = 'CHF'
    CAD = 'CAD'
    HKD = 'HKD'
    SEK = 'SEK'
    NZD = 'NZD'
    KRW = 'KRW'
    SGD = 'SGD'
    NOK = 'NOK'
    MXN = 'MXN'
    INR = 'INR'


class FormatType(util.Constant):
    NUMBER = 'Number'
    STRING = 'String'
    URL = 'URL'
    DATE = 'Date'
    CURRENCY = 'Currency'
    PHONE = 'Phone'
    EMAIL = 'Email'


class Field(collections.MutableMapping):
    """Represent a Field object -- used by both AppleTemplate and
    GoogleTemplate to represent data/information on a template.
    """
    GOOGLE_LABEL_MAP = {
        GoogleFieldType.INFO_MODULE: 'label',
        GoogleFieldType.TEXT_MODULE: 'header',
        GoogleFieldType.LINKS_MODULE: 'description',
        GoogleFieldType._IMAGE_MODULE: 'imageDescription',
        GoogleFieldType.POINTS_MODULE: 'label',
        GoogleFieldType.NOT_ASSIGNED: 'label',
        GoogleFieldType.TITLE_MODULE: 'description.string',
        GoogleFieldType.ACCOUNT_MODULE: 'label',
        GoogleFieldType._LOYALTY_POINTS: 'label'
    }
    GOOGLE_VALUE_MAP = {
        GoogleFieldType.INFO_MODULE: 'value',
        GoogleFieldType.TEXT_MODULE: 'body',
        GoogleFieldType.LINKS_MODULE: 'uri',
        GoogleFieldType._IMAGE_MODULE: 'image',
        GoogleFieldType.POINTS_MODULE: 'balance',
        GoogleFieldType.NOT_ASSIGNED: 'value',
        GoogleFieldType.TITLE_MODULE: 'title.string',
        GoogleFieldType.ACCOUNT_MODULE: 'value',
        GoogleFieldType._LOYALTY_POINTS: 'balance'
    }

    def __init__(self, name=None, **kwargs):
        if not name:
            raise ValueError('Must set field name.')
        self.name = name
        self.field_values = {}
        for key, val in kwargs.iteritems():
            self[key] = val

    # Serialization / Deserialization methods for Apple & Google
    @classmethod
    def build_apple_field(cls, name, data):
        """Create a Field from an Apple-based field dictionary.

        Arguments:
            name (string): The field name (e.g. 'Reward Points')
            data (dict): The field dictionary.

        Raises:
            ValueError

        Returns:
            A Field object.

        Example:
            >>> Field.build_apple_field('Reward Points', {
            ...     'changeMessage': None,
            ...     'label': 'Points',
            ...     'hideEmpty': False,
            ...     'formatType': 'String',
            ...     'value': '1234.0',
            ...     'fieldType': 'header',
            ...     'required': False,
            ...     'order': 1
            ... }
            <Field name:Reward Points, fieldType:header>
        """
        AppleFieldType.validate(data.get('fieldType'))
        return cls(name, **data)

    @classmethod
    def build_google_field(cls, name, data):
        """Create a Field from a Google-based module dictionary.

        Arguments:
            name (string): The field name (e.g. 'Reward Points')
            data (dict): The field dictionary.

        Returns:
            A Field object.

        Example:
            >>> Field.build_google_field('Points', {
            ...     'col': 1,
            ...     'row': 0,
            ...     'label': 'Points',
            ...     'hideEmpty': False,
            ...     'formatType': 'String',
            ...     'balance': '1234.0',
            ...     'fieldType': 'pointsModuleData'
            ... }
            <Field name:Points, fieldType:header>
        """
        GoogleFieldType.validate(data.get('fieldType'), allow_private=True)
        field = cls(name, **data)

        # Post processing for google: convert row/col to order if possible.
        row, col = field.get('row'), field.get('col')
        row_col = [row, col]
        if 0 in row_col and not None in row_col:
            del field['row']
            del field['col']
            field['order'] = field._row_col_to_order(row, col)
        return field

    def build_apple_json(self):
        """Take a field object, fill in necessary blanks for serialization.

        Returns:
            A dictionary representing a field object for an Apple Template.
            Will attempt to infer formatType and numberStyle if not specified
            by the caller.

        Example:
            >>> f = Field(
            ...     name='Points',
            ...     label='Points',
            ...     value=1234,
            ...     fieldType=AppleFieldType.HEADER
            ... )
            >>> f.build_apple_json()
            {
                'label': 'Points',
                'value': 1234,
                'fieldType': 'header',
                'formatType': 'Number',
                'numberStyle': 'numberStyleDecimal'
            }
        """
        if self['fieldType'] == GoogleFieldType.NOT_ASSIGNED:
            return self.field_values

        payload = copy.deepcopy(self.field_values)
        if (
            payload.get('formatType') == 'Number' and
            not payload.get('numberStyle')
        ):
            payload['numberStyle'] = self._infer_number_style(self['value'])
        return payload

    def build_google_template_json(self):
        """This function converts a field object into a properly-formatted
        Google template field.

        Returns:
            A dictionary representing a field (module item) object for a Google
            Template. Will automatically convert value/label to the appropriate
            keys given the module type (e.g., header/body for TEXT_MODULE).

        Example:
            >>> f = Field(
            ...     name='Some Text',
            ...     label='Points',
            ...     value=1234,
            ...     fieldType=GoogleFieldType.TEXT_MODULE
            ... )
            >>> f.serialize_to_google()
            {'header': 'label', 'body': 1234, 'fieldType': 'textModule',
             'formatType': 'Number'}
        """
        if self['fieldType'] == GoogleFieldType.NOT_ASSIGNED:
            return self.field_values

        payload = {}
        for key, value in self.field_values.iteritems():
            if key == 'label':
                payload[self.GOOGLE_LABEL_MAP[self['fieldType']]] = value
            elif key == 'value':
                payload[self.GOOGLE_VALUE_MAP[self['fieldType']]] = value
            else:
                payload[key] = value
        payload = self._common_google_processing(payload)
        return payload

    def _build_common_template_json(self):
        """Common serialization items. Things that happen for both Apple
        and Google.

        .. note::

            * If currencyCode is specified and formatType isn't, validate
            currencyCode and set formatType to 'Currency'.
            * If formatType isn't specified, use the general _infer_format_type
            method to guess.
            * If no order is specified, default to 1.
            * If no fieldType is specified, default to ``notAssigned``.

        Returns:
            A dict object -- represents key val pairs not represented directly
            in the object but that can be inferred from the object data.
        """
        if self.get('currencyCode'):
            CurrencyCode.validate(self['currencyCode'])
            self['formatType'] = 'Currency' if not self.get('formatType') else self['formatType']
        if not self.get('formatType') and self.get('value'):
            self['formatType'] = self._infer_format_type(self['value'])
        if not self.get('order'):
            self['order'] = 1
        if not self.get('fieldType'):
            self['fieldType'] = 'notAssigned'

    def build_google_pass_json(self):
        """This function converts a field object into a properly-formatted
        Google pass field.

        Returns:
            A dictionary representing a field (module item) object for a Google
            Pass.

        Example:
            >>> f = Field(
            ...     name='Some Text',
            ...     label='Points',
            ...     value=1234,
            ...     fieldType=GoogleFieldType.TEXT_MODULE
            ... )
            >>> f.serialize_to_google()
            {'label': 'Points', 'value': 1234, 'fieldType': 'textModule'}
        """
        payload = copy.deepcopy(self.field_values)
        return self._common_google_processing(payload)

    def build_pass_json(self):
        """When creating a field for a pass, there may be no way to
        determine the fieldType. This method builds json for fields
        where the vendor/fieldType may be unknown.

        """
        try:
            # Handle known google fields
            GoogleFieldType.validate(self.get('fieldType'))
            return self.build_google_pass_json()
        except ValueError:
            pass

        try:
            AppleFieldType.validate(self.get('fieldType'))
            return self.build_apple_json()
        except ValueError:
            pass

        return self.field_values

    # Apple/Google Helper functions
    @staticmethod
    def _infer_number_style(value):
        """In the case of a number field, determine the number style. There's
        no real way to determine if numberStylePercent is the intended
        numberStyle.
        """
        if isinstance(value, float) or isinstance(value, int):
            return NumberStyle.DECIMAL
        elif isinstance(value, basestring):
            if 'E' in value or 'e' in value:
                return NumberStyle.SCIENTIFIC
            return NumberStyle.TEXT
        else:
            raise ValueError('Unrecognized number value: {}'.format(value))

    @staticmethod
    def _row_col_to_order(row, col):
        """Convert rows/cols (legacy) to order. (Google only)
        """
        if row == 0 and col == 0:
            return 1
        elif row == 0:
            return col + 1
        else:
            return row + 1

    @staticmethod
    def _infer_format_type(value):
        """Determine the format type of the field, if not declared
        explicitly. (Apple and Google).

        Notes:
            Should guess correctly in most cases, but formatType can always
            be overridden  by the user.
        """
        if isinstance(value, basestring):
            # Int/float values
            try:
                int(value)
                return 'Number'
            except ValueError:
                pass

            try:
                # Handles scientific notation as well.
                float(value)
                return 'Number'
            except ValueError:
                pass

            # Date values
            try:
                datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                return 'Date'
            except ValueError:
                pass

            # URL values
            url = parse.urlparse(value)
            if url.scheme != '' and url.netloc != '':
                return 'URL'

            return 'String'
        elif isinstance(value, float) or isinstance(value, int):
            return 'Number'
        else:
            raise ValueError('Unrecognized value type: {}'.format(type(value)))

    @staticmethod
    def _common_google_processing(payload):
        if (
            payload.get('order') and
            payload.get('fieldType') == GoogleFieldType.TEXT_MODULE
        ):
            # Special case: Order does not work in text modules -- must
            # reconvert to rows/cols.
            payload['col'], payload['row'] = 0, payload['order'] - 1
            del payload['order']
        return payload

    # Dictionary implementation
    def __setitem__(self, key, value):
        # Convert Google label/value pairs to standard label, value
        if key in Field.GOOGLE_LABEL_MAP.values():
            key = FieldKey.LABEL
        if key in Field.GOOGLE_VALUE_MAP.values():
            key = FieldKey.VALUE
        # Catch an invalid key
        FieldKey.validate(key)

        # Catch an invalid value
        if key == FieldKey.TEXT_ALIGNMENT:
            TextAlignment.validate(value)
            self.field_values[key] = value
        elif key == FieldKey.FORMAT_TYPE:
            FormatType.validate(value)
            self.field_values[key] = value
        elif key == FieldKey.NUMBER_STYLE:
            # Convert number style from PKNumberStyle to numberStyle, if necessary.
            value = value.replace('PKN', 'n')
            NumberStyle.validate(value)
            self.field_values[key] = value
        # Convert loyaltyPoints to pointsModule
        elif key == FieldKey.FIELD_TYPE:
            util.check_multiple(value, AppleFieldType, GoogleFieldType)
            if value == GoogleFieldType._LOYALTY_POINTS:
                self.field_values[key] = GoogleFieldType.POINTS_MODULE
            else:
                self.field_values[key] = value
        else:
            self.field_values[key] = value

    def __getitem__(self, key):
        return self.field_values[key]

    def __iter__(self):
        return iter(self.field_values)

    def __len__(self):
        return len(self.field_values)

    def __delitem__(self, key):
        del self.field_values[key]

    # Additional magic methods
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.field_values == other.field_values and self.name == other.name

    def __repr__(self):
        return '<Field name:{}, fieldType:{}>'.format(
            self.name,
            self.get('fieldType')
        )
