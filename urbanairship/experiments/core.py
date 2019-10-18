from urbanairship import common
import json


class AB_test(object):
    def __ini__(self, airship):
        self.airship = airship

    def _get_listing(self, url, limit=None):
        """List experiments

        :keyword limit: Optional, maximum number of experiments,
        default is 10, max is 100
        """

        params = {}
        if isinstance(limit, int):
            params['limit'] = limit

        response = self.airship.request(
            method='GET',
            body=None,
            params=params,
            url=url,
            version=3
        )
        return response

    def list_experiments(self, _body_builder_):
        url = common.EXPERIMENTS_URL
        return self._get_listing(url)

    def create(self, experiment):
        """ Create an experiment """

        url = common.EXPERIMENTS_URL
        body = json.dumps(experiment.payload)
        response = self.airship.request(
            method='POST',
            body=body,
            url=url,
            content_type='aplication/json',
            version=3
        )
        return response
        
    def list_scheduled_experiment(self):
        url = common.EXPERIMENTS_SCHEDULE_URL
        return self._get_listing(url)

    def delete(self, experiment_id):
        """ Delete a scheduled experiment. You can only delete experiments before they start
        
        :keyword experiment_id: The unique identifier of the experiment, type string
        DELETE /api/experiments/scheduled/{experiment_id}
        """
        url = common.EXPERIMENTS_SCHEDULE_URL + experiment_id
        response = self.airship.request(
            method='DELETE',
            body=None,
            url=url,
            version=3
        )

        return response

    def validate(self):
        pass

    def lookup(self):
        pass
