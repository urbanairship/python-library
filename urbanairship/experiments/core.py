from urbanairship import common


class Experiment(object):

    def list_experiments(self, limit=None):
        """List experiments

        :keyword limit: Optional, maximum number of experiments, 
        default is 10, max is 100
        """

        params = {}
        if isinstance(limit, int):
            params['limit'] = limit

        url = common.EXPERIMENTS_URL
        response = self.airship.request(
            method='GET',
            body=None,
            params=params,
            url=url,
            version=3
        )
   
        return response

    def create(self):
        pass

    def list_scheduled_experiment(self):
        pass

    def delete(self):
        pass

    def validate(self):
        pass

    def lookup(self):
        pass
