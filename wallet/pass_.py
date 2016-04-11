from .template import *
import copy
import numbers

###########################################################

class PassStatus:
    """
        Enum for the life cycle status for a pass
    """
    ALL = 'all'                                     # List all passes
    INSTALLED = 'installed'                         # List all installed passes
    UNINSTALLED = 'uninstalled'                     # List all uninstalled passes
    BEEN_INSTALLED = 'been_installed'               # List all passes that have at one point been installed
    NOT_BEEN_INSTALLED = 'not_been_installed'       # List all passes that have never been installed


###########################################################

class Pass(Template):
    """
        A pass object represents an installable pass
        It has many shared properties with @see Template
    """

    def __init__(self, template, pass_type=None, vendor=Vendor.APPLE):
        """
            This creates a pass object either from a template or through a template id

            If a template object is passed it will inherit many properties from the templates
            Including names, fields and other properties.

            :param template: template object or template id
            :param pass_type: one of the TemplateTypes or (or inherited from template)
            :param vendor: Vendor.Google or Vendor.Apple (or inherited from template)
           :return:
        """
        super(Pass, self).__init__(None, None, pass_type, vendor, None)

        if isinstance(template, Template):
            self.unpack_dict(copy.copy(template.get_dict()))
            self.template_id = template.id
        elif isinstance(template, numbers.Integral):
            self.template_id = template
        else:
            raise ValueError('The template needs to be a high level object or an integer')

        self.tags = []

    """

        @name.setter
        def name(self, name):
            raise Warning('Name cannot be set on the pass level')

        @type.setter
        def type(self, type):
            raise Warning('Type cannot be set on the pass level')
    """

    @property
    def id(self):
        return self.val('id')

    @property
    def serial_number(self):
        return self.val('serialNumber')

    @property
    def status(self):
        return self.val('status')

    @property
    def url(self):
        return self.val('url')

    @property
    def expiration_date(self):
        return self.val('expirationDate')

    @expiration_date.setter
    def expiration_date(self, expiration_date):
        self.add_header_property('expirationDate', expiration_date)

    @property
    def public_url(self):
        return self.val('publicUrl').get('path')

    @property
    def pass_image(self):
        return self.val('publicUrl').get('image')

    @property
    def public_url_type(self):
        return self.get('publicUrl').val('type')

    @public_url.setter
    def public_url_type(self, type):
        self.set('publicUrl', {'type': type})

    def set_public_url_type_single(self):
        self.public_url_type = 'single'

    def set_public_url_type_multiple(self):
        self.public_url_type = 'multiple'

    @property
    def template_id(self):
        return self.val('templateId')

    @template_id.setter
    def template_id(self, template_id):
        self.set('templateId', template_id)

    def add_tag(self, tag):
        for t in self.tags:
            if t == tag:
                return False

        self.tags.append(tag)
        return True

    def delete_tag(self, tag):
        try:
            self.remove(tag)
            return True
        except ValueError:
            return False

    ############################## API FUNCTIONS  ##############################

    def create(self, wallet_object, template_id=None, external_id=None):
        if template_id is None:
            if self.template_id is None:
                raise ValueError('No template id specified')
            else:
                template_id = self.template_id

        return wallet_object.create_pass(self, template_id, external_id)

    def update(self, wallet_object):
        return wallet_object.update_pass(self, self.id)

    def delete(self, wallet_object):
        return wallet_object.delete_pass(self.id)

    @classmethod
    def get(cls, wallet_object, pass_id):
        return Pass.from_dict(wallet_object.get_pass(pass_id))

    ############################## CLASSMETHODS ##############################

    @classmethod
    def from_dict(cls, obj_dict):
        """
            Creates a template or pass object from json download.
            Use this from the response of get_template for example
        """

        ret = cls(template=0)
        ret.unpack_dict(create_uploadable_template_from_downloaded_template(obj_dict))
        if ret.vendor == Vendor.GOOGLE:
            ret.fix_google_fields_after_download()

        return ret

