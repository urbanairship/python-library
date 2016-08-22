import logging
import json

from wallet import common


logger = logging.getLogger('urbanairship')


def get_template(wallet, template_id=None, external_id=None):
    """Retrieve a template.

    Arguments:
        wallet (obj): A wallet client object.
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
    response = wallet.request(
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
    logger.info('Successfully retrieved template {}.'.format(
        template_id if template_id else external_id
    ))
    return Template.from_data(payload)


def delete_template(wallet, template_id=None, external_id=None):
    """Delete a template.

    Arguments:
        wallet (obj): A UA Wallet object.
        template_id (str or int): The ID of the template you wish to delete.
        external_id (str or int): The external ID of the template you wish
            to delete.

    Returns:
        A boolean representing success.

    Raises:
        ValueError: If neither, or both, of template_id and external_id
            are specified.

    Example:
        >>> delete_template(ua_wallet, template_id=123456)
        True
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = wallet.request(
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


def duplicate_template(wallet, template_id=None, external_id=None):
    """Duplicate a template.

    Arguments:
        wallet (obj): A UA Wallet object.
        template_id (str or int): The ID of the template you wish to delete.
        external_id (str or int): The external ID of the template you wish
            to delete.

    Returns:
        A dictionary containing the id of the newly created template.

    Raises:
        ValueError: If neither, or both, of template_id and external_id
            are specified.

    Example:
        >>> duplicate_template(ua_wallet, template_id=12345)
        {'templateId': 12346}
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = wallet.request(
        method='POST',
        body=None,
        url=Template.build_url(
            common.TEMPLATE_DUPLICATE_URL,
            main_id=template_id,
            external_id=external_id
        ),
        version=1.2
    )
    logger.info('Successful template deletion: {}'.format(
        template_id if template_id else external_id
    ))
    return response.json()


def add_template_locations(
    wallet, locations, template_id=None, external_id=None):
    """Add locations to a template.

    Arguments:
        wallet (Wallet object): A wallet client object.
        locations (list of dicts): A list of location objects, represented
            as dictionaries.
        template_id (str): The ID of the template you wish to add
            locations to.
        external_id (str): The external ID of the template you wish to add
            locations to.

    Returns:
        A list of objects containing the location value, locationId,
            and fieldId.

    Raises:
        ValueError: If neither, or both of, template_id and external_id
            are specified.

    Example:
        >>> add_template_locations(
        ...     ua_wallet, [location1, location2], template_id=12345
        ... )
        [{'value': { '...' }, 'locationId': 12345, 'fieldId': 54321},
         {'value': { '...' }, 'locationId': 56789, 'fieldId': 98765}]
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = wallet.request(
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
    logger.info('Successfully added {} locations to template {}.'.format(
        len(locations),
        template_id if template_id else external_id
    ))
    return response.json()


def remove_template_location(
        wallet, location_id, template_id=None, external_id=None
):
    """Remove a location from a template

    Arguments:
        wallet (Wallet object): A wallet client object.
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
        >>> remove_template_location(ua_wallet, 12345, template_id=44444)
        True
    """
    if not (template_id or external_id) or (template_id and external_id):
        raise ValueError(
            'Please specify only one of template_id or external_id.'
        )

    response = wallet.request(
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
    logger.info('Successfully removed location {} from template {}.'.format(
        location_id,
        template_id if template_id else external_id
    ))
    return True


class Template(object):

    @classmethod
    def from_data(cls, data):
        """Create a template from a JSON payload.
        """
        return data

    @staticmethod
    def build_url(url, main_id=None, external_id=None, location_id=None):
        if location_id:
            if main_id:
                return url.format(main_id, location_id)
            else:
                return url.format('id/' + str(external_id), location_id)
        else:
            if main_id and external_id:
                return url.format(str(main_id) + '/id/' + str(external_id))
            elif main_id:
                return url.format(main_id)
            else:
                return url.format('id/' + str(external_id))


class TemplateList(common.IteratorParent):
    """Forms a template listing request.

    Arguments:
        wallet (Wallet client): The wallet client object.
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
            self, wallet, page_size=None, page=None, order=None, direction=None
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
        super(TemplateList, self).__init__(wallet, params)


class AppleTemplate(object):

    def __init__(self):
        self.url = None
        self.template_id = None

    @classmethod
    def from_data(cls, data):
        template = cls()
        template.headers = data.get("fieldsModel", {}).get("headers")
        if not template.headers:
            raise ValueError("missing headers")
        template.fields = data.get("fieldsModel", {}).get("fields")
        if not template.fields:
            raise ValueError("missing fields")
        template.beacons = data.get("fieldsModel", {}).get("beacons")
        template.locations = data.get("userlocations")
        template.templateHeaders = data["templateHeader"]

        return template

    def create_payload(self):
        payload = {"headers": {}, "fields": {}}
        for k, v in self.headers.iteritems():
            payload["headers"][k] = v

        for k, v in self.fields.iteritems():
            payload["fields"][k] = v

        for k, v in self.templateHeaders.iteritems():
            payload[k] = v

        if "userlocations" in payload:
            for k, v in self.locations:
                payload["userlocations"][k] = v

        for field in payload["fields"]:
            for key, value in payload["fields"][field].items():
                if key == "numberStyle":
                    new_value = value.replace("PKNumberStyle", "numberStyle")
                    payload["fields"][field][key] = new_value

        return payload
