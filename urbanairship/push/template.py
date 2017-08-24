import logging
import datetime

from urbanairship import common

logger = logging.getLogger('urbanairship')


class TemplateInfo(object):
    """Information object for a template.

    # TODO: add ivars here

    """

    template_id = None
    created_at = None
    modified_at = None
    last_used = None
    name = None
    description = None
    variables = None
    push = None

    @classmethod
    def from_payload(cls, payload, template_key):
        """Create based on results from a TemplateList iterator."""
        obj = cls()
        obj.template_id = payload[template_key]
        for key in payload:
            if key in ('created_at', 'modified_at', 'last_used'):
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], '%Y-%m-%dT%H:%M:%S.%fZ'
                    )
                except:
                    payload[key] = "UNKNOWN"
            setattr(obj, key, payload[key])
        return obj

    @classmethod
    def lookup(cls, airship, template_id):
        """Fetch metadata from a template ID"""
        start_url = common.TEMPLATES_URL
        data_attribute = 'template'
        id_key = 'id'
        params = {}
        url = start_url + template_id
        response = airship._request(
            method='GET',
            body=None,
            url=url,
            version=3,
            params=params
        )
        payload = response.json()
        return cls.from_payload(payload[data_attribute], id_key)


class TemplateList(common.IteratorParent):
    """Iterator for listing all templates for this application.

    :ivar limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`TemplateInfo` object.

    """
    next_url = common.TEMPLATES_URL
    data_attribute = 'templates'
    id_key = 'id'
    instance_class = TemplateInfo

    def __init__(self, airship, limit=None):
        params = {'limit': limit} if limit else {}
        super(TemplateList, self).__init__(airship, params)


# TODO: create template, update template, delete template

def merge_data(template_id, substitutions):
    """Template push merge_data creation.

    :param template_id: Required, UUID.
    :param substitutions: Required, dictionary of template variables and their
        substitutions, e.g. {"FIRST_NAME": "Bob", "LAST_NAME": "Smith"}

    """

    md = {}

    md['template_id'] = template_id
    md['substitutions'] = {
        key: val for key, val in iter(substitutions.items()) if val is not None
    }

    return md
