import json
from typing import Any, Dict, Optional

from requests import Response

from urbanairship.client import BaseClient
from urbanairship.experiments.experiment import Experiment


class ABTest(object):
    def __init__(self, airship: BaseClient):
        self.airship = airship

    def _get_listing(self, url: str, limit: Optional[int] = None) -> Response:
        """List experiments

        :keyword limit: Optional, maximum number of experiments,
        default is 10, max is 100
        """

        params: Dict[str, Any] = {}
        if isinstance(limit, int):
            params["limit"] = limit

        response = self.airship.request(
            method="GET", body=None, params=params, url=url, version=3
        )
        return response

    def list_experiments(self) -> Response:
        """List experiments, sorted by created_at date/time from newest to oldest

        :keyword limit: Positive maximum number of elements to return per page.
            Default limit is 10. Max: 100 and Min: 1.
        """
        url = self.airship.urls.get("experiments_url")
        return self._get_listing(url)

    def create(self, experiment: Experiment) -> Response:
        """Create an experiment"""

        url = self.airship.urls.get("experiments_url")
        body = json.dumps(experiment.payload)
        response = self.airship.request(
            method="POST",
            body=body,
            url=url,
            content_type="application/json",
            version=3,
        )
        return response

    def list_scheduled_experiment(self) -> Response:
        """List scheduled experiments in order, from closest to the current
        date-time to farthest"""

        url = self.airship.urls.get("experiments_schedule_url")
        return self._get_listing(url)

    def delete(self, experiment_id: str) -> Response:
        """Delete a scheduled experiment. You can only delete experiments before they start

        :keyword experiment_id: The unique identifier of the experiment, type string
        """

        url = self.airship.urls.get("experiments_schedule_url") + "/" + experiment_id
        response = self.airship.request(method="DELETE", body=None, url=url, version=3)

        return response

    def validate(self, experiment: Experiment) -> Response:
        """Accepts the same range of payloads as /api/experiments,
        but only parses and validates the payload without creating the experiment.
        An experiment may validate and still fail to be delivered. For example,
        you may have a valid experiment with no devices in your audience.

        :keyword experiment: Body of the experiment you want to validate
        """
        url = self.airship.urls.get("experiments_validate")
        body = json.dumps(experiment.payload)
        response = self.airship.request(
            method="POST",
            body=body,
            url=url,
            content_type="application/json",
            version=3,
        )

        return response

    def lookup(self, experiment_id: str) -> Response:
        """Look up an experiment (A/B Test)

        :keyword experiment_id: The unique identifier of the experiment, type string
        """

        url = self.airship.urls.get("experiments_url") + "/" + experiment_id
        response = self.airship.request(method="GET", body=None, url=url, version=3)

        return response
