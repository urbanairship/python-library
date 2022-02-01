from typing import Dict, Any

from urbanairship import Airship


class ExperimentReport(object):
    def __init__(self, airship: Airship) -> None:
        """Access reporting related to A/B Tests (experiments)

        :param airship: An urbanairship.Airship instance.
        """
        self.airship = airship

    def get_overview(self, push_id: str) -> Dict[str, Any]:
        """Returns statistics and metadata about an experiment (A/B Test).

        :param push_id:  A UUID representing an A/B test of the requested experiment.

        :returns: JSON from the API
        """
        url = self.airship.urls.get("reports_url") + "experiment/overview/{0}".format(
            push_id
        )

        response = self.airship._request("GET", None, url, version=3)

        return response.json()

    def get_variant(self, push_id: str, variant_id: str) -> Dict[str, Any]:
        """Returns statistics and metadata about a specific variant in an experiment (A/B Test).

        :param push_id: A UUID representing an A/B test of the requested experiment.
        :param variant_id: An integer represennting the variant requested.

        :returns: JSON from the API
        """
        url = self.airship.urls.get("reports_url") + "experiment/detail/{0}/{1}".format(
            push_id, variant_id
        )

        response = self.airship._request("GET", None, url, version=3)

        return response.json()
