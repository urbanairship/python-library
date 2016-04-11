from .wict import Wict

class TextAlign:
    LEFT = 'textAlignmentLeft'
    CENTER = 'textAlignmentCenter'
    RIGHT = 'textAlignmentRight'
    NATURAL = 'textAlignmentNatural'


class NumberStyle:
    DECIMAL = 'numberStyleDecimal'
    PERCENT = 'numberStylePercent'
    SCIENTIFIC = 'numberStyleScientific'
    SPELLED_OUT = 'numberStyleSpellOut'


class FormatType:
    STRING = 'String'
    NUMBER = 'Number'
    CURRENCY = 'Currency'
    DATE = 'Date'
    URL = 'URL'

###########################################################

class AppleFieldLocation:
    """
        These are the various pass locations for an Apple pass.
        The location within each of these locations are specified
        by the order parameter
    """
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    TERTIARY = 'tertiary'
    AUXILIARY = 'auxiliary'
    BACK = 'back'
    HEADER = 'header'


class GoogleFieldLocation:
    """
        These are the various pass locations for a Google pass.
        The location within each of these locations are specified
        by the order parameter
    """
    TITLE_MODULE = 'titleModule'
    ACCOUNT_MODULE = 'acctModule'
    POINTS_MODULE = 'pointsModule'
    LINKS_MODULE = 'linksModuleData'
    TEXT_MODULE = 'textModulesData'
    INFO_MODULE = 'infoModuleData'


###########################################################


class Field(Wict):
    """
        A field on a template or pass

        Apple and Google fields are different due to different location names.
    """

    # These fix the strange label/value mapping differences depending on where on a pass you are

    LABEL_NAMES_LOCATION_MAPPING = {
        AppleFieldLocation.PRIMARY: 'label',
        AppleFieldLocation.SECONDARY: 'label',
        AppleFieldLocation.AUXILIARY: 'label',
        AppleFieldLocation.TERTIARY: 'label',
        AppleFieldLocation.BACK: 'label',
        AppleFieldLocation.HEADER: 'label',

        GoogleFieldLocation.TITLE_MODULE: 'title.string',
        GoogleFieldLocation.ACCOUNT_MODULE: 'label',
        GoogleFieldLocation.POINTS_MODULE: 'label',
        GoogleFieldLocation.LINKS_MODULE: 'description',
        GoogleFieldLocation.TEXT_MODULE: 'header',
        GoogleFieldLocation.INFO_MODULE: 'label'
    }

    VALUE_NAMES_LOCATION_MAPPING = {

        AppleFieldLocation.PRIMARY: 'value',
        AppleFieldLocation.SECONDARY: 'value',
        AppleFieldLocation.AUXILIARY: 'value',
        AppleFieldLocation.TERTIARY: 'value',
        AppleFieldLocation.BACK: 'value',
        AppleFieldLocation.HEADER: 'value',

        GoogleFieldLocation.TITLE_MODULE: 'description.string',
        GoogleFieldLocation.ACCOUNT_MODULE: 'label',
        GoogleFieldLocation.POINTS_MODULE: 'balance',
        GoogleFieldLocation.LINKS_MODULE: 'uri',
        GoogleFieldLocation.TEXT_MODULE: 'body',
        GoogleFieldLocation.INFO_MODULE: 'label'
    }

    def __init__(self, name, label, value, location, format_type, order=1):
        super(Field, self).__init__()
        self.location = location
        self.name = name
        self.label = label
        self.value = value
        self.format_type = format_type
        self.order = order

    @property
    def label(self):
        return self.val(self.LABEL_NAMES_LOCATION_MAPPING[self.location])

    @label.setter
    def label(self, label):
        self.set(self.LABEL_NAMES_LOCATION_MAPPING[self.location], label)

    @property
    def value(self):
        return self.val(self.VALUE_NAMES_LOCATION_MAPPING[self.location])

    @value.setter
    def value(self, value):
        self.set(self.VALUE_NAMES_LOCATION_MAPPING[self.location], value)

    @property
    def location(self):
        return self.val('fieldType')

    @location.setter
    def location(self, location):
        self.set('fieldType', location)

    @property
    def format_type(self):
        return self.val('formatType')

    @format_type.setter
    def format_type(self, format_type):
        self.set('formatType', format_type)

    @property
    def order(self):
        return self.val('order')

    @order.setter
    def order(self, order):
        self.set('order', order)
        self.set('row', order - 1)

    @property
    def change_message(self):
        return self.val('changeMessage')

    @change_message.setter
    def change_message(self, change_message):
        self.set('changeMessage', change_message)

###########################################################

class TextField(Field):
    def __init__(self, name, label, value, location, order=1, text_alignment=TextAlign.LEFT):
        super(TextField, self).__init__(name, label, value, location, FormatType.STRING, order)
        self.text_alignment = text_alignment

    @property
    def text_alignment(self):
        return self.val('textAlignment')

    @text_alignment.setter
    def text_alignment(self, text_alignment):
        self.set('textAlignment', text_alignment)

class NumberField(Field):
    def __init__(self, name, label, value, location, order=1, number_style=NumberStyle.DECIMAL):
        super(NumberField, self).__init__(name, label, value, location, FormatType.NUMBER, order)
        self.number_style = number_style

    @property
    def number_style(self):
        return self.val('numberStyle')

    @number_style.setter
    def number_style(self, number_style):
        self.set('numberStyle', number_style)

class DateField(Field):
    def __init__(self, name, label, value, location, order=1):
        super(DateField, self).__init__(name, label, value, location, FormatType.DATE, order)

class CurrencyField(Field):
    def __init__(self, name, label, value, location, order=1, currency_code='USD'):
        super(CurrencyField, self).__init__(name, label, value, location, FormatType.CURRENCY, order)
        self.currency_code = currency_code

    @property
    def currency_code(self):
        return self.val('currencyCode')

    @currency_code.setter
    def currency_code(self, currency_code):
        self.set('currencyCode', currency_code)


class URLField(Field):
    def __init__(self, name, label, value, location, order=1):
        super(URLField, self).__init__(name, label, value, location, FormatType.URL, order)

###########################################################

def field_factory_from_dict(field_data):
    mapping_dict = {FormatType.STRING: (TextField, {'text_alignment': None}),
                    FormatType.CURRENCY: (CurrencyField, {'currency_code': None}),
                    FormatType.DATE: (DateField, {}),
                    FormatType.NUMBER: (NumberField, {'number_style': None}),
                    FormatType.URL: (URLField, {})
                    }

    field_kwargs = {'name': None, 'label': None, 'value': None, 'location': AppleFieldLocation.PRIMARY}

    func = mapping_dict[field_data['formatType']]
    field_kwargs.update(func[1])
    ret = func[0](**field_kwargs)
    ret.unpack_dict(field_data)
    return ret
