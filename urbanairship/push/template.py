import datetime
import json
import logging
from typing import Dict, List, Optional, Any, Type

from requests import Response

from urbanairship import common, Airship
from urbanairship.push.core import Push


logger = logging.getLogger("urbanairship")


class Template(object):
    """Information object for a template.

    :keyword template_id: UUID; the ID of this template, set automatically.
    :keyword created_at: UTC datetime when the template was created.
    :keyword modified_at: UTC datetime when the template was last modified.
    :keyword last_used: UTC datetime when the template was last used for a push
        notification. Will be set to 'UNKNOWN' if never used.
    :keyword name: Required, name of the template, set during
        creation/modification.
    :keyword description: Optional, description of the template, set during
        creation/modification.
    :keyword variables: Required, an array of `Template Variable Objects
        <https://docs.urbanairship.com/api/ua/#template-variable-object>`_.
    :keyword push: Optional, a  push specification object, as defined by the `Push
        Object specification
        <https://docs.urbanairship.com/api/ua/#push-object>`_, but does not
        include ``audience`` or ``device_types`` since those are set when push
        messages are sent. Message Center ``message`` is also not supported in
        Templates at this time.

    """

    def __init__(
        self,
        airship: Airship,
        name: Optional[str] = None,
        description: Optional[str] = None,
        variables: Optional[List[Dict[str, Any]]] = None,
        push: Optional[Type[Push]] = None,
    ) -> None:
        self.airship = airship
        self._template_id: Optional[str] = None
        self._created_at: Optional[datetime.datetime] = None
        self._modified_at: Optional[datetime.datetime] = None
        self._last_used: Optional[datetime.datetime] = None
        self.name = name
        self.description = description
        self.variables = variables
        self.push = push

    @property
    def template_id(self) -> Optional[str]:
        return self._template_id

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        return self._created_at

    @property
    def modified_at(self) -> Optional[datetime.datetime]:
        return self._modified_at

    @property
    def last_used(self) -> Optional[datetime.datetime]:
        return self._last_used

    @property
    def payload(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "name": self.name,
            "variables": self.variables,
            "push": self.push,
        }
        if self.description is not None:
            data["description"] = self.description
        return data

    def create(self) -> Response:
        """Create a notification template with the API.

        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """

        if not self.name:
            raise ValueError("Must set name before template creation.")

        if not self.push:
            raise ValueError("Must set push before template creation.")

        body = json.dumps(self.payload)
        response = self.airship._request(
            method="POST",
            body=body,
            url=self.airship.urls.get("templates_url"),
            content_type="application/json",
            version=3,
        )
        self._template_id = response.json().get("template_id")
        logger.info("Successful template creation for template %s", self.template_id)

        return response

    def update(self, template_id: Optional[str] = None) -> Response:
        """Update a template with the API.

        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """

        update_payload: Dict[str, Any] = {}

        if (
            not self.name
            and not self.description
            and not self.push
            and not self.variables
        ):
            raise ValueError(
                "Must set at least one of name, description, push, or "
                "variables before template update."
            )

        if self.name:
            update_payload["name"] = self.name

        if self.description:
            update_payload["description"] = self.description

        if self.push:
            update_payload["push"] = self.push

        if self.variables:
            update_payload["variables"] = self.variables

        if not template_id and not self.template_id:
            raise ValueError("Cannot update template without ID.")
        if template_id:
            self._template_id = template_id

        body = json.dumps(update_payload)
        response = self.airship._request(
            method="POST",
            body=body,
            url=f"{self.airship.urls.get('templates_url')}{self.template_id}",
            content_type="application/json",
            version=3,
        )
        logger.info("Successful template update for template %s", self.template_id)

        return response

    def delete(self, template_id: Optional[str] = None) -> Response:
        """Delete a previously created template.

        :raises AirshipFailure: Request failed.
        :raises Unauthorized: Authentication failed.

        """

        if not template_id and not self.template_id:
            raise ValueError("Cannot delete template without ID.")
        if template_id:
            self._template_id = template_id

        response = self.airship._request(
            method="DELETE",
            body=None,
            url=f'{self.airship.urls.get("templates_url")}{self.template_id}',
            version=3,
        )
        logger.info("Successful template delete for template %s", self.template_id)

        return response

    @classmethod
    def from_payload(cls, payload, id_key, airship):
        """Create based on results from a TemplateList iterator."""
        obj = cls(airship)
        obj._template_id = payload[id_key]
        for key in payload:
            if key in ("created_at", "modified_at", "last_used"):
                try:
                    payload[key] = datetime.datetime.strptime(
                        payload[key], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                except:
                    payload[key] = "UNKNOWN"
                setattr(obj, "_" + key, payload[key])
            elif key == "template_id":
                obj._template_id = payload[key]
            else:
                setattr(obj, key, payload[key])
        return obj

    def lookup(self, template_id):
        """Fetch metadata from a template ID"""
        start_url = self.airship.urls.get("templates_url")
        data_attribute = "template"
        id_key = "id"
        params = {}
        url = start_url + template_id
        response = self.airship._request(
            method="GET", body=None, url=url, version=3, params=params
        )
        payload = response.json()
        return self.from_payload(payload[data_attribute], id_key, self.airship)


class TemplateList(common.IteratorParent):
    """Iterator for listing all templates for this application.

    :keyword limit: Number of entries to fetch in each page request.
    :returns: Each ``next`` returns a :py:class:`Template` object.

    """

    next_url: Optional[str] = None
    data_attribute: str = "templates"
    id_key: str = "id"
    instance_class: Type[Template] = Template

    def __init__(self, airship, limit=None):
        params = {"limit": limit} if limit else {}
        self.next_url = airship.urls.get("templates_url")
        super(TemplateList, self).__init__(airship, params)


def merge_data(template_id: str, substitutions: Dict[str, Any]) -> Dict[str, Any]:
    """Template push merge_data creation.

    :param template_id: Required, UUID.
    :param substitutions: Required, dictionary of template variables and their
        substitutions, e.g. {"FIRST_NAME": "Bob", "LAST_NAME": "Smith"}

    """

    md: Dict[str, Any] = {}

    md["template_id"] = template_id
    md["substitutions"] = {
        key: val for key, val in iter(substitutions.items()) if val is not None
    }

    return md
