import logging

from wallet import common

logger = logging.getLogger('urbanairship')


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

        # if "beacons" in payload:
        #     for k, v in self.beacons:
        #         payload["beacons"][k] = v

        for field in payload["fields"]:
            for key, value in payload["fields"][field].items():
                if key == "numberStyle":
                    new_value = value.replace("PKNumberStyle", "numberStyle")
                    payload["fields"][field][key] = new_value

        return payload
