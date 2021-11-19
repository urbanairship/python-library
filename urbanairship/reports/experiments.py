class ExperimentReport(object):
    def __init__(self, airship):
        self.airship = airship

    def get_overview(self, push_id):
        url = self.airship.urls.get("reports_url") + "experiment/overview/{0}".format(
            push_id
        )

        response = self.airship._request("GET", None, url, version=3)

        return response.json()

    def get_variant(self, push_id, variant_id):
        url = self.airship.urls.get("reports_url") + "experiment/detail/{0}/{1}".format(
            push_id, variant_id
        )

        response = self.airship._request("GET", None, url, version=3)

        return response.json()
