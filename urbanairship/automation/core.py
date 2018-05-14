from urbanairship import common
import json


class Automation(object):
    def __init__(self, airship):
        self.airship = airship

    def create(self, pipelines):
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
        url = common.PIPELINES_URL + pipeline_id
        response = self.airship.request(
            method='DELETE',
            body=None,
            url=url,
            version=3
        )

        return response

    def lookup(self, pipeline_id):
        url = common.PIPELINES_URL + pipeline_id
        response = self.airship.request(
            method='GET',
            body=None,
            url=url,
            version=3
        )

        return response

    def list_automations(self, limit=None, enabled=None):
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
