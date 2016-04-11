from .wallet import Wallet
from .template import *
from .project import Project
from .pass_ import Pass


###########################################################

class WalletIterable(object):
    """
        Base iterator class for all API list operations. Do not use this directly. Use the subclasses for each type!
    """

    def __init__(self, wallet_object, list_function=None, list_name=None, list_param=None, json_factory=None,
                 page_size=None, page_number=0, order_by=None, sort_direction=None):
        """
            :param wallet_object: The wallet object to operate on
            :param list_function: Wallet function to retrieve the paginated list
            :param list_name:  The JSON response list name for example 'projects'
            :param json_factory: The object JSON factory

            The rest of the parameters are normal pagination controls
        """

        self.list_function = list_function
        self.list_param = list_param
        self.list_name = list_name
        self.json_factory = json_factory
        self.wallet_object = wallet_object
        self.obj = {}
        self.list = []
        self.total_count = 2
        self.current = 0
        self.current_stop = 0
        self.current_page_index = 0
        self.page_size = page_size
        self.page_number = page_number
        self.order_by = order_by
        self.sort_direction = sort_direction

    def get_list(self):
        if self.list_param is not None:
            self.obj = self.list_function(self.wallet_object, self.list_param, page_number=self.page_number,
                                          page_size=self.page_size, order_by=self.order_by,
                                          sort_direction=self.sort_direction)
        else:
            self.obj = self.list_function(self.wallet_object, page_number=self.page_number, page_size=self.page_size,
                                          order_by=self.order_by, sort_direction=self.sort_direction)

        self.total_count = self.obj['count']
        self.list = self.obj[self.list_name]
        self.page_size = self.obj['pagination']['pageSize']
        self.current = self.obj['pagination']['start']
        self.current_stop = self.current + self.page_size
        self.current_page_index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current >= self.total_count:
            raise StopIteration

        if self.current >= self.current_stop:
            self.page_number += 1
            self.get_list()
            if self.current >= self.total_count:
                raise StopIteration

        self.current += 1
        self.current_page_index += 1
        return self.json_factory(self.list[self.current_page_index - 1])


###########################################################

class ProjectIterable(WalletIterable):
    """
        Allows retrieving projects and iterate over them
        @see List
    """

    def __init__(self, wallet_object, page_size=None, page_number=0, order_by=None, sort_direction=None):
        super(ProjectIterable, self).__init__(wallet_object, list_name='projects', list_function=Wallet.list_projects,
                                              list_param=None, json_factory=Project.from_dict, page_size=page_size,
                                              page_number=page_number, order_by=order_by, sort_direction=sort_direction)


###########################################################

class TemplateIterable(WalletIterable):
    """
        Allows retrieving templates and iterate over them
        @see List
    """

    def __init__(self, wallet_object, page_size=None, page_number=0, order_by=None, sort_direction=None):
        super(TemplateIterable, self).__init__(wallet_object, list_name='templateHeaders',
                                               list_function=Wallet.list_templates, list_param=None,
                                               json_factory=Template.from_dict, page_size=page_size,
                                               page_number=page_number, order_by=order_by,
                                               sort_direction=sort_direction)


###########################################################

class PassIterable(WalletIterable):
    """``
        Allows retrieving passes and iterate over them
        @see List
    """

    def __init__(self, wallet_object, template_id, page_size=None, page_number=0, order_by=None, sort_direction=None):
        super(PassIterable, self).__init__(wallet_object, list_name='passes', list_function=Wallet.list_passes,
                                           list_param=template_id, json_factory=Pass.from_dict, page_size=page_size,
                                           page_number=page_number, order_by=order_by, sort_direction=sort_direction)

###########################################################
