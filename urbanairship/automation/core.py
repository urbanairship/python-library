import json
from typing import List, Union, Optional

from urbanairship import Airship
from urbanairship.automation.pipeline import Pipeline
from requests import Response


class Automation(object):
    """An object for getting and creating automations.

    :keyword airship: An urbanairship.Airship instance,
         instantiated with the key corresponding to the airship project you wish
         to use.
    """

    def __init__(self, airship: Airship) -> None:
        self.airship = airship

    def create(self, pipelines: Union[Pipeline, List[Pipeline]]) -> Response:
        """Create an automation with one or more Pipeline payloads

        :keyword pipelines: A single Pipeline payload or list of Pipeline payloads
        """
        url = self.airship.urls.get("pipelines_url")
        body = json.dumps(pipelines)
        response = self.airship.request(
            method="POST",
            body=body,
            url=url,
            content_type="application/json",
            version=3,
        )

        return response

    def validate(self, pipelines: Union[Pipeline, List[Pipeline]]) -> Response:
        """Validate a Pipeline payloads

        :keyword pipelines: A single Pipeline payload or list of Pipeline payloads
        """
        url = self.airship.urls.get("pipelines_url") + "validate/"
        body = json.dumps(pipelines)
        response = self.airship.request(
            method="POST",
            body=body,
            url=url,
            content_type="application/json",
            version=3,
        )

        return response

    def update(self, pipeline_id: str, pipeline: Pipeline) -> Response:
        """Update an existing Automation Pipeline

        :keyword pipeline_id: A Pipeline ID
        :keyword pipeline: Full Pipeline payload; partial updates are not supported
        """
        url = self.airship.urls.get("pipelines_url") + pipeline_id
        body = json.dumps(pipeline)
        response = self.airship.request(
            method="PUT", body=body, url=url, content_type="application/json", version=3
        )

        return response

    def delete(self, pipeline_id: str) -> Response:
        """Delete an existing Automation Pipeline

        :keyword pipeline_id: A Pipeline ID
        """
        url = self.airship.urls.get("pipelines_url") + pipeline_id
        response = self.airship.request(method="DELETE", body=None, url=url, version=3)

        return response

    def lookup(self, pipeline_id: str) -> Response:
        """Lookup an Automation Pipeline

        :keyword pipeline_id: A Pipeline ID
        """
        url = self.airship.urls.get("pipelines_url") + pipeline_id
        response = self.airship.request(method="GET", body=None, url=url, version=3)

        return response

    def list_automations(
        self, limit: Optional[int] = None, enabled: bool = False
    ) -> Response:
        """List active Automations

        :keyword limit: Optional, maximum pipelines to return
        :keyword enabled: Optional, boolean limiter for results to only enabled
            Pipelines
        """
        params = {}
        if isinstance(limit, int):
            params["limit"] = limit
        if isinstance(enabled, bool):
            params["enabled"] = enabled

        url = self.airship.urls.get("pipelines_url")
        response = self.airship.request(
            method="GET", body=None, params=params, url=url, version=3
        )

        return response

    def list_deleted_automations(self, start: Optional[str] = None) -> Response:
        """List deleted Automation Pipelines

        :keyword start: Optional starting timestamp for limiting results in ISO-8601
            format
        """
        params = {}
        if start:
            params["start"] = start
        url = self.airship.urls.get("pipelines_url") + "deleted/"
        response = self.airship.request(
            method="GET", body=None, params=params, url=url, version=3
        )

        return response
