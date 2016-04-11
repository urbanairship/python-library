import requests
import os
import json
import logging
import numbers
from . import __about__
from .template import Template
from .location import Location
from .wict import Wict

"""     (c) Urban Airship 2016      """

logger = logging.getLogger('urbanairship')

###########################################################

class SortDirection:
    """
        Enum for sorting direction of returned lists use with Sort_order
    """
    ASCENDING = 'ASC'  # Get query sorted in ascending order (Default)
    DESCENDING = 'DESC'  # Get query sorted in descending order


class SortOrder:
    """
        Enum for sorting by key of returned lists use with Sort_direction
    """
    ID = 'id'  # Sort query according to id (Default)
    NAME = 'name'  # Sort query according to name
    CREATED_AT = 'createdAt'  # Sort query according to creation time
    UPDATED_AT = 'updatedAt'  # Sort query according to update time

class Path:
    """
        Defines for RESTful paths
    """
    ID = 'id/'  # Denotes an external id instead of a normal id
    PROJECT = 'project/'
    TEMPLATE = 'template/'
    APPLE = 'apple/'
    PASS = 'pass/'
    TAG = 'tag/'
    UPLOAD = 'upload/'

    TAGS = '/tags'
    PASSES = '/passes'


###########################################################

class Wallet(object):
    """

        Wallet Restful API class

        Implement client side access of:

        http://docs.urbanairship.com/api/wallet.html

        See docs for details about JSON payload used in many of these functions
        or even better use the high level classes for API access

    """

    lib_version = __about__.__version__

    headers = {
        'Api-Revision': '1.2',
        'Content-Type': 'application/json',
        'User-agent': 'PythonLib-' + lib_version
    }

    def __init__(self, api_key=None, debug_on=False, url=None):
        """
            :param api_key: Your API key (You can set it in env as UA_API_KEY)
            :param debug_on: Turn on debugging
            :param host: URL to the server. Do not set
            :return: the wallet object
        """
        if debug_on:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        if api_key is None:
            api_key = os.getenv('UA_API_KEY', None)

        if api_key is None:
            api_key = os.getenv('UA_API_KEY_PROD', None)

        if api_key is None:
            logger.error('API key is not defined. Provide it either with parameter and environment variable')

        if url is None:
            url = 'https://wallet-api.urbanairship.com'

        self.api_key = api_key
        self.url = url

    ###########################################################
    #              Helpers and constructors                   #
    ###########################################################

    def call_wallet_api(self, req_func, path, body='', optional_params='', return_binary=False, includes_v1=True,
                        optional_headers=None):
        """
            Generic function to call the Wallet API
            :param req_func: requests.get, request.post, request.put, requests.delete
            :param path: restful path example: 'template/123'
            :param body: any other request parameters
            :return: json response
        """

        url = '{0}/{1}{2}?api_key={3}{4}'.format( self.url, 'v1/' if includes_v1 else '', path, self.api_key,
                                                  optional_params)

        headers = self.headers.copy()
        if optional_headers is not None:
            headers.update(optional_headers)

        args = {
            'data': body,
            'url': url,
            'headers': headers
        }

        logger.info('{0} {1}/v1/{2}?api_key=X{3}'.format(req_func.__name__.upper(), self.url, path, optional_params))

        r = req_func(**args)
        if r.status_code != requests.codes.ok and r.status_code != 201:
            logger.error("ERROR: unsuccessful request with response code: " + str(r.status_code))
            logger.error(r.content)
            r.raise_for_status()

        if return_binary:
            return r.content

        return r.json()

    @classmethod
    def _add_external_id(cls, path, external_id):
        if external_id is not None:
            return path + Path.ID + external_id
        return path

    @classmethod
    def _add_project_id(cls, path, project_id):
        if project_id is not None:
            return path + '/' + str(project_id)
        return path

    @classmethod
    def _handle_potential_external_id(cls, path, external_id):
        if not str(external_id).isdigit():
            return Wallet._add_external_id(path, external_id)
        return path + str(external_id)

    @classmethod
    def _handle_ordering_params(cls, page_size, page_number, order_by, sort_direction):

        ret = ''
        if page_size is not None:
            if isinstance(page_size, numbers.Integral) and page_size > 0:
                ret += '&pageSize=' + str(page_size)
            else:
                raise ValueError('Page size needs to be a positive integer')

        if page_number is not None:
            if isinstance(page_number, numbers.Integral) and page_number > 0:
                ret += '&page=' + str(page_number)
            else:
                raise ValueError('Page number needs to be a positive integer')

        if order_by is not None:
            if any(order_by in o for o in [SortOrder.Id, SortOrder.NAME, SortOrder.CREATED_AT, SortOrder.UPDATED_AT]):
                ret += '&order=' + order_by
            else:
                raise ValueError('Invalid sort order by')

        if sort_direction is not None:
            if any(sort_direction in d for d in [SortDirection.ASCENDING, SortDirection.DESCENDING]):
                ret += '&direction=' + sort_direction
            else:
                raise ValueError('Sort Direction is either SortDirection.ASCENDING/DESCENDING')

        return ret

    @classmethod
    def _fix_payload(cls, payload):
        """
        Allows the various API functions to accept a JSON dictionary,
        a JSON string or a high level API object
        """
        if isinstance(payload, basestring):
            return payload
        elif isinstance(payload, dict):
            return json.dumps(payload)
        elif isinstance(payload, Wict):
            if isinstance(payload, Template):
                payload.fix_google_fields_for_upload()

            return payload.to_json()
        else:
            raise ValueError('Unable to convert payload to JSON')

    @classmethod
    def _update_object(cls, obj, response_dict):
        """
            Updates the high level object dict if it exists
            with the response from the call
        """
        if isinstance(obj, Wict):
            obj.get_dict().update(response_dict)
            if isinstance(obj, Template):
                obj.fix_google_fields_after_download()

        return response_dict

    @classmethod
    def _convert_list(cls, lst, list_name):
        """
            Converts list of high level objects or strings to a dict with the list as an object
            with key list_name
            :param lst: the list
            :param list_name: the key the dictionary of the list
            :return: dictionary
        """
        if isinstance(lst, list):
            return {list_name: [item.get_dict() if isinstance(item, Location) else str(item) for item in lst]}
        return lst


    ###########################################################
    #                   Restful Calls                         #
    ###########################################################

    def create_project(self, payload, external_id=None):
        return Wallet._update_object(payload, self.call_wallet_api(requests.post,
                                                                    Wallet._add_external_id(Path.PROJECT,
                                                                                             external_id),
                                                                    body=Wallet._fix_payload(payload)))

    def list_projects(self, page_size=None, page_number=None, order_by=None, sort_direction=None):
        return self.call_wallet_api(requests.get, Path.PROJECT,
                                    optional_params=Wallet._handle_ordering_params(page_size, page_number, order_by,
                                                                                    sort_direction))

    def get_project(self, project_id):
        return self.call_wallet_api(requests.get,
                                    Wallet._handle_potential_external_id(Path.PROJECT, project_id))

    def update_project(self, payload, project_id):
        return self.call_wallet_api(requests.put,
                                    Wallet._handle_potential_external_id(Path.PROJECT, project_id),
                                    body=Wallet._fix_payload(payload))

    def delete_project(self, project_id):
        return self.call_wallet_api(requests.delete,
                                    Wallet._handle_potential_external_id(Path.PROJECT, project_id))

    ###########################################################

    def create_template(self, payload, project_id, external_id=None):
        return Wallet._update_object(payload, self.call_wallet_api(requests.post, Wallet._add_external_id(
            Path.TEMPLATE + str(project_id) + '/', external_id), body=Wallet._fix_payload(payload)))

    def list_templates(self, page_size=None, page_number=None, order_by=None, sort_direction=None):
        return self.call_wallet_api(requests.get, Path.TEMPLATE + 'headers',
                                    optional_params=Wallet._handle_ordering_params(page_size, page_number, order_by,
                                                                                    sort_direction))

    def get_template(self, template_id):
        return self.call_wallet_api(requests.get,
                                    Wallet._handle_potential_external_id(Path.TEMPLATE, template_id))

    def update_template(self, payload, template_id):
        return self.call_wallet_api(requests.put,
                                    Wallet._handle_potential_external_id(Path.TEMPLATE, template_id),
                                    body=Wallet._fix_payload(payload))

    def delete_template(self, template_id):
        return self.call_wallet_api(requests.delete,
                                    Wallet._handle_potential_external_id(Path.TEMPLATE, template_id))

    ###########################################################

    def list_passes(self, template_id, status=None, page_size=None, page_number=None, order_by=None,
                    sort_direction=None):
        optional = Wallet._handle_ordering_params(page_size, page_number, order_by, sort_direction)

        if status is not None:
            optional += '&status=' + status

        return self.call_wallet_api(requests.get, Path.TEMPLATE + str(template_id) + Path.PASSES,
                                    optional_params=optional)

    def create_pass(self, payload, template_id, pass_id=None):
        path = Path.PASS + str(template_id) + '/'
        path = Wallet._handle_potential_external_id(path, pass_id)
        return Wallet._update_object(payload,
                                     self.call_wallet_api(requests.post, path, body=Wallet._fix_payload(payload)))

    def update_pass(self, payload, pass_id):
        ret = self.call_wallet_api(requests.put, Wallet._handle_potential_external_id(Path.PASS, pass_id),
                                   body=Wallet._fix_payload(payload))
        return ret['ticketId']

    def get_pass(self, pass_id):
        return self.call_wallet_api(requests.get, Wallet._handle_potential_external_id(Path.PASS, pass_id))

    def delete_pass(self, pass_id):
        return self.call_wallet_api(requests.delete, Wallet._handle_potential_external_id(Path.PASS, pass_id))


    ###########################################################
