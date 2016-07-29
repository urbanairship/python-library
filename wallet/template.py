import logging

from wallet import common


logger = logging.getLogger('urbanairship')


class TemplateList(common.IteratorParent):
    """Forms a template listing request.

    Arguments:
        wallet (Wallet client): The wallet client object.
        page_size (int): The size of each page of the template listing
            response. Defaults to 10.
        page (int): The page to start the listing response on. Defaults
            to 1.
        order (string): The attribute used to order the templates. Can be one of
            ``"id"``, ``"name"``, ``"createdAt"``, or ``"updatedAt"``.
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

    def __init__(self, wallet, page_size=None, page=None, order=None, direction=None):
        if direction not in [None, 'ASC', 'DESC']:
            raise ValueError(
                'Unrecognized direction {}. Please use one of \'ASC\' or \'DESC\''.format(direction)
            )
        params = {
            'pageSize': page_size,
            'page': page,
            'order': order,
            'direction': direction
        }
        params = {k: v for k, v in params.iteritems() if v != None}
        super(TemplateList, self).__init__(wallet, params)


class AppleTemplate(object):
    def __init__(self):
        self.url = None
        self.template_id = None

    @classmethod
    def get_from_id(cls, wallet, template_id):
        """ Load an existing template based on the provided templateId. """
        url = common.TEMPLATE_URL.format(template_id)
        response = wallet.request(
            method='GET',
            body=None,
            url=url,
            version=1.2
        )
        payload = response.json()
        return cls.from_data(payload)

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
