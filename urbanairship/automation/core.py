from urbanairship import common
import json


class Automation(object):
    """An object for getting and creating automations"""

    def __init__(self, airship):
        self.airship = airship

    def create(self, pipelines):
        """Create an automation with one or more Pipeline payloads

        :keyword pipelines: A single Pipeline payload or list of Pipeline
        payloads
        """
        url = common.PIPELINES_URL
        body = json.dumps(pipelines)
        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            content_type='application/json',
            version=3
        )

        return response

    def validate(self, pipelines):
        """Validate a Pipeline payloads

        :keyword pipelines: A single Pipeline payload or list of Pipeline
        payloads
        """
        url = common.PIPELINES_URL + 'validate/'
        body = json.dumps(pipelines)
        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            content_type='application/json',
            version=3
        )

        return response

    def update(self, pipeline_id, pipeline):
        """Update an existing Automation Pipeline

        :keyword pipeline_id: A UA Pipeline ID
        :keyword pipeline: Full Pipeline payload; partial updates are not
        supported
        """
        url = common.PIPELINES_URL + pipeline_id
        body = json.dumps(pipeline)
        response = self.airship.request(
            method='PUT',
            body=body,
            url=url,
            content_type='application/json',
            version=3
        )

        return response

    def delete(self, pipeline_id):
        """Delete an existing Automation Pipeline

        :keyword pipeline_id: A UA Pipeline ID
        """
        url = common.PIPELINES_URL + pipeline_id
        response = self.airship.request(
            method='DELETE',
            body=None,
            url=url,
            version=3
        )

        return response

    def lookup(self, pipeline_id):
        """Lookup an Automation Pipeline

        :keyword pipeline_id: A UA Pipeline ID
        """
        url = common.PIPELINES_URL + pipeline_id
        response = self.airship.request(
            method='GET',
            body=None,
            url=url,
            version=3
        )

        return response

    def list_automations(self, limit=None, enabled=False):
        """List active Automations

        :keyword limit: Optional, maximum pipelines to return
        :keyword enabled: Optional, boolean limiter for results to only enabled
        Pipelines
        """
        params = {}
        if isinstance(limit, int):
            params['limit'] = limit
        if isinstance(enabled, bool):
            params['enabled'] = enabled

        url = common.PIPELINES_URL
        response = self.airship.request(
            method='GET',
            body=None,
            params=params,
            url=url,
            version=3
        )

        return response

    def list_deleted_automations(self, start=None):
        """List deleted Automation Pipelines

        :keyword start: Optional, starting timestamp for limiting results;
        ISO-8601 format
        """
        params = {}
        if start:
            params['start'] = start
        url = common.PIPELINES_URL + 'deleted/'
        response = self.airship.request(
            method='GET',
            body=None,
            params=params,
            url=url,
            version=3
        )

        return response
