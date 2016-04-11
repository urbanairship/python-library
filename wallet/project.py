from .wict import Wict
import copy
###########################################################

class ProjectType:
    """
        These are the different types of project types
        Each project can only hold the templates of the
        corresponding type

        @see TemplateType
    """
    LOYALTY = 'loyalty'
    COUPON = 'coupon'
    OFFER = 'offer'
    GIFT_CARD = 'giftCard'
    MEMBER_CARD = 'memberCard'
    EVENT_TICKET = 'eventTicket'
    BOARDING_PASS = 'boardingPass'
    GENERIC = 'generic'


###########################################################

class Project(Wict):
    """
        The project object represents the Wallet concept of a Project
        that hosts the template objects and some general settings.


        Example JSON:
                {
                      "name": "Aztec Barcode",
                      "projectType": "loyalty",
                      "description": "Aztec Barcode",
                      "settings": {
                        "barcode_alt_text": "123json=456789",
                        "barcode_label": "Member ID",
                        "barcode_default_value": "123456789",
                        "barcode_encoding": "iso-8859-1",
                        "barcode_type": "pdf417"
                      }
                }
    """

    def __init__(self, name, pass_type, description=None):
        super(Project, self).__init__()
        self.name = name
        self.project_type = pass_type
        self.description = description

    @property
    def id(self):
        return self.val('id')

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
    def project_type(self):
        return self.val('projectType')

    @project_type.setter
    def project_type(self, project_type):
        self.set('projectType', project_type)

    @property
    def description(self):
        return self.val('description')

    @description.setter
    def description(self, description):
        self.set('description', description)

    @classmethod
    def from_dict(cls, obj_dict):
        ret = cls(name=None, pass_type=None)
        ret.unpack_dict(obj_dict)
        return ret

    ############################## API FUNCTIONS  ##############################

    def create(self, wallet_object, external_id=None):
        return wallet_object.create_project(self, external_id)

    def update(self, wallet_object):
        return wallet_object.update_project(self, self.id)

    def delete(self, wallet_object):
        return wallet_object.delete_project(self.id)

    @classmethod
    def get(cls, wallet_object, project_id):
        return Project.from_dict(wallet_object.get_project(project_id))

