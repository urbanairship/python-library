import json


class SubscriptionList(object):
    """
    Subscribe or unsubscribe channels to/from Subscription lists. These lists must
    be created in the Airship web dashboard prior to making these calls. The
    value for list_id can be found after creating these lists.

    :param airship: Required. An urbanairship.Airship instance.
    :param list_id: Required. The list_id from the Airship web dashboard.
    """

    def __init__(self, airship, list_id):
        self.airship = airship
        self.list_id = list_id

    def unsubscribe(self, audience):
        """
        Unsubscribe an audience from a subscription list.

        :param audience: Required. A single audience selector (ex:
            urbanairship.ios_channel) to unsubscribe.
        """
        payload = {
            "subscription_lists": {"action": "unsubscribe", "list_id": self.list_id},
            "audience": audience,
        }

        response = self.airship.request(
            method="POST",
            body=json.dumps(payload).encode("utf-8"),
            url=self.airship.urls.get("subscription_lists_url"),
            version=3,
        )

        return response

    def subscribe(self, audience):
        """
        Subscribe an audience from a subscription list.

        :param list_id: Required. The list_id from the Airship web dashboard.
        :param audience: Required. A single audience selector (ex:
            urbanairship.ios_channel) to subscribe.
        """
        payload = {
            "subscription_lists": {"action": "subscribe", "list_id": self.list_id},
            "audience": audience,
        }

        response = self.airship.request(
            method="POST",
            body=json.dumps(payload).encode("utf-8"),
            url=self.airship.urls.get("subscription_lists_url"),
            version=3,
        )

        return response
