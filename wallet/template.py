from .convenience import *
from .field import *
from .location import *
from .wict import Wict

###########################################################

class TemplateType:
    """
        These are the various template types
        Note that some of them are shared between
        Android and iOS and some are specific
        Refer to the appropriate documentation

        @see ProjectType
    """
    BOARDING_PASS = 'Boarding Pass'
    COUPON = 'Coupon'
    EVENT_TICKET = 'Event Ticket'
    GENERIC = 'Generic'
    STORE_CARD = 'Store Card'
    LOYALTY = 'Loyalty'
    OFFER = 'Offer'
    GIFT_CARD = 'Gift Card'


###########################################################

class Vendor:
    """
        Which Pass vendor the template and passes are for
        Supported types are Apple and Google
    """
    GOOGLE = 'Google'
    APPLE = 'Apple'


###########################################################

class Template(Wict):
    """
        A template object represents a pass template
    """

    def __init__(self, project_id, name, template_type, vendor=Vendor.APPLE, description="No description"):
        super(Template, self).__init__()
        self.set('fields', {})
        self.set('headers', {})
        self.set('beacons', [])
        self.set('locations', [])
        self.name = name
        self.template_type = template_type
        self.project_id = project_id
        self.vendor = vendor
        self.description = description
        try:
            self.icon_image
        except KeyError:
            self.icon_image = 'https://s3.amazonaws.com/passtools-localhost/1/images/default-pass-icon.png'

    @property
    def id(self):
        # Fixing templateId inconsistency where the template functions returns strange things
        if self.has_key('id'):
            return self.val('id')
        return self.val('templateId')

    @property
    def created_at(self):
        return self.val('createdAt')

    @property
    def updated_at(self):
        return self.val('updatedAt')

    @property
    def name(self):
        return self.val('name')

    @name.setter
    def name(self, name):
        self.set('name', name)

    @property
    def template_type(self):
        return self.val('type')

    @template_type.setter
    def template_type(self, template_type):
        self.set('type', template_type)

    @property
    def project_id(self):
        return self.val('projectId')

    @project_id.setter
    def project_id(self, project_id):
        self.set('projectId', project_id)

    @property
    def expiry_duration(self):
        return self.val('expiryDuration')

    @expiry_duration.setter
    def expiry_duration(self, expiry_duration):
        self.set('expiryDuration', expiry_duration)

    @property
    def vendor(self):
        return self.val('vendor')

    @vendor.setter
    def vendor(self, vendor):
        self.set('vendor', vendor)

        if vendor == Vendor.APPLE:
            self.set('vendorId', 1)
        elif vendor == Vendor.GOOGLE:
            self.set('vendorId', 2)
        else:
            raise ValueError('Unknown vendor ' + str(vendor))

    @property
    def description(self):
        return self.val('description')

    @description.setter
    def description(self, description):
        self.set('description', description)

    ############################## HEADER PROPERTIES ##############################

    def add_header_property(self, name, value, location='topLevel'):
        headers = self.val('headers')
        headers[name] = {}
        headers[name]['formatType'] = 1
        headers[name]['fieldType'] = location
        headers[name]['value'] = value

    def get_header_property(self, name):
        headers = self.val('headers')
        if name in headers and 'value' in headers[name]:
            return headers[name]['value']

        raise KeyError('Error: Cannot find key ' + name)

    @property
    def label_color(self):
        return self.get_header_property('logo_color')

    @label_color.setter
    def label_color(self, label_color_str):
        self.add_header_property('logo_color', label_color_str)

    def set_label_color(self, red, green, blue):
        self.label_color = Template.get_color_string(red, green, blue)

    @property
    def value_color(self):
        return self.get_header_property('foreground_color')

    @value_color.setter
    def value_color(self, value_color_str):
        self.add_header_property('foreground_color', value_color_str)

    def set_value_color(self, red, green, blue):
        self.value_color = Template.get_color_string(red, green, blue)

    @property
    def background_color(self):
        return self.get_header_property('background_color')

    @background_color.setter
    def background_color(self, background_color_str):
        self.add_header_property('background_color', background_color_str)

    def set_background_color(self, red, green, blue):
        self.background_color = Template.get_color_string(red, green, blue)

    @property
    def thumbnail_image(self):
        return self.get_header_property('thumbnail_image')

    @thumbnail_image.setter
    def thumbnail_image(self, thumbnail_image):
        self.add_header_property('thumbnail_image', thumbnail_image, 'image')

    @property
    def background_image(self):
        return self.get_header_property('background_image')

    @background_image.setter
    def background_image(self, background_image):
        self.add_header_property('background_image', background_image, 'image')

    @property
    def icon_image(self):
        return self.get_header_property('icon_image')

    @icon_image.setter
    def icon_image(self, icon_image):
        self.add_header_property('icon_image', icon_image, 'image')

    @property
    def logo_image(self):
        return self.get_header_property('logo_image')

    @logo_image.setter
    def logo_image(self, logo_image):
        self.add_header_property('logo_image', logo_image, 'image')

    @property
    def strip_image(self):
        return self.get_header_property('strip_image')

    @strip_image.setter
    def strip_image(self, strip_image):
        self.add_header_property('strip_image', strip_image, 'image')

    @property
    def footer_image(self):
        return self.get_header_property('footer_image')

    @footer_image.setter
    def footer_image(self, footer_image):
        self.add_header_property('footer_image', footer_image, 'image')

    @property
    def barcode_type(self):
        return self.get_header_property('barcode_type')

    @barcode_type.setter
    def barcode_type(self, barcode_type):
        self.add_header_property('barcode_type', barcode_type, 'barcode')

    @property
    def barcode_value(self):
        return self.get_header_property('barcode_value')

    @barcode_value.setter
    def barcode_value(self, barcode_value):
        self.add_header_property('barcode_value', barcode_value, 'barcode')

    @property
    def barcode_label(self):
        return self.get_header_property('barcode_label')

    @barcode_label.setter
    def barcode_label(self, barcode_label):
        self.add_header_property('barcode_label', barcode_label, 'barcode')

    @property
    def barcode_encoding(self):
        return self.get_header_property('barcode_encoding')

    @barcode_encoding.setter
    def barcode_encoding(self, barcode_encoding):
        self.add_header_property('barcode_encoding', barcode_encoding, 'barcode')

    @property
    def barcode_alt_text(self):
        return self.get_header_property('barcodeAltText')

    @barcode_alt_text.setter
    def barcode_alt_text(self, barcode_alt_text):
        self.add_header_property('barcodeAltText', barcode_alt_text, 'barcode')

    def add_barcode(self, barcode_type, barcode_value, barcode_label="", barcode_encoding='iso-8859-1',
                    barcode_alt_text=None):
        self.barcode_type = barcode_type
        self.barcode_value = barcode_value
        self.barcode_label = barcode_label
        self.barcode_encoding = barcode_encoding
        if barcode_alt_text is not None:
            self.barcode_alt_text = barcode_alt_text

    ######################## FIELDS/BEACONS/LOCATIONS ###########################

    @property
    def fields(self):
        return self.val('fields')

    @fields.setter
    def fields(self, fields):
        self.set('fields', fields)

    def add_field(self, field):
        self.val('fields')[field.name] = field.get_dict()

    def get_field(self, field_name):
        field = field_factory_from_dict(self.val('fields')[field_name])
        field.name = field_name
        return field

    def delete_field(self, field_name):
        ret = self.val('fields').pop(field_name)
        return ret

    @property
    def locations(self):
        return [Location.from_dict(self.val('locations')[location]) for location in self.val('locations')]

    @locations.setter
    def locations(self, locations):
        ex = 'Locations cannot be added through the normal template API.'
        ex += 'To add locations pass a list of locations to: add_locations_template'
        raise ValueError(ex)

    ############################## API FUNCTIONS ##############################

    def create(self, wallet_object, project_id=None, external_id=None):
        if project_id is None:
            if self.project_id is None:
                raise ValueError('No project id specified')
            else:
                project_id = self.project_id

        return wallet_object.create_template(self, project_id, external_id)

    def update(self, wallet_object):
        return wallet_object.update_template(self, self.id)

    def delete(self, wallet_object):
        return wallet_object.delete_template(self.id)

    @classmethod
    def get(cls, wallet_object, template_id):
        return Template.from_dict(wallet_object.get_template(template_id))

    ############################## HELPERS ##############################

    GOOGLE_FIELD_DICTIONARIES = [GoogleFieldLocation.TITLE_MODULE, GoogleFieldLocation.ACCOUNT_MODULE,
                                 GoogleFieldLocation.POINTS_MODULE, GoogleFieldLocation.TEXT_MODULE,
                                 GoogleFieldLocation.INFO_MODULE, GoogleFieldLocation.LINKS_MODULE]

    @classmethod
    def get_color_string(cls, red, green, blue):
        return 'rgb(' + str(red) + ',' + str(green) + ',' + str(blue) + ')'

    @classmethod
    def from_dict(cls, obj_dict):
        """
            Creates a template or pass object from json download.
            Use this from the response of get_template for example
        """
        ret = cls(project_id=None, name=None, template_type=None)
        ret.unpack_dict(create_uploadable_template_from_downloaded_template(obj_dict))
        if ret.vendor == Vendor.GOOGLE:
            ret.fix_google_fields_after_download()
        return ret

    def fix_google_fields_after_download(self):
        """
            Moves google fields into the main fields
        """
        self.set('fields', {})
        if self.vendor == Vendor.GOOGLE:
            for dict_name in Template.GOOGLE_FIELD_DICTIONARIES:
                if dict_name in self.get_dict():
                    for key, value in self.val(dict_name).iteritems():
                        if value['fieldType'] == 'loyaltyPoints':  # Fix points module inconsistency
                            value['fieldType'] = GoogleFieldLocation.POINTS_MODULE
                        self.val('fields')[key] = value
                    self.set(dict_name, None)

    def fix_google_fields_for_upload(self):
        """
            Moves google fields into the various dictionaries for API call
        """
        if self.vendor == Vendor.GOOGLE:
            for dict_name in Template.GOOGLE_FIELD_DICTIONARIES:
                self.set(dict_name, {})

            # put the fields in the correct dictionary
            for key, value in self.fields.iteritems():
                new_key = value['fieldType']
                if new_key == GoogleFieldLocation.POINTS_MODULE:  # Fix points module inconsistency
                    value['fieldType'] = 'loyaltyPoints'

                self.val(new_key)[key] = value

            self.fields = {}

###########################################################
