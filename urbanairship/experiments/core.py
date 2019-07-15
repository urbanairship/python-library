from urbanairship import common


class Experiment(object):

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
 
    def create(self):
        pass

    def list_scheduled_experiment(self):
        url = common.EXPERIMENTS_SCHEDULE_URL
        return self._get_listing(url)

    def delete(self):
        pass

    def validate(self):
        pass

    def lookup(self):
        pass
