import json
from typing import Any, Dict, List, Optional, Union, cast

from urbanairship.client import OAuthClient

TRIGGERING_ID = Union[str, List[str]]


class Journeys:
    """A class for entering and exiting audiences from a Sequence (Journey).

    Please see the documentation at
    https://docs.airship.com/api/ua/#tag-journeys for details on Journeys usage.

    .. note::

        The ``/api/journeys/trigger`` and ``/api/journeys/exit`` endpoints only
        support OAuth2 authentication. This class must be instantiated with an
        ``urbanairship.OAuthClient``; passing any other client raises a
        ``TypeError``.

    :param airship: [required] An ``urbanairship.OAuthClient`` instance.
    """

    def __init__(self, airship: OAuthClient) -> None:
        if not isinstance(airship, OAuthClient):
            raise TypeError(
                "Journeys endpoints only support OAuth2 authentication. "
                "airship must be an urbanairship.OAuthClient instance."
            )
        self.airship = airship

    @staticmethod
    def _validate_triggering_id(triggering_id: TRIGGERING_ID) -> TRIGGERING_ID:
        """Validate a triggering_id value. Accepts a single string or a list of
        1 to 10 strings, matching the API's oneOf constraint."""
        if isinstance(triggering_id, str):
            return triggering_id

        if isinstance(triggering_id, list):
            if not 1 <= len(triggering_id) <= 10:
                raise ValueError("triggering_id must contain between 1 and 10 items when a list")
            if not all(isinstance(item, str) for item in triggering_id):
                raise ValueError("each triggering_id must be a string")
            return triggering_id

        raise TypeError("triggering_id must be a string or a list of strings")

    def trigger(
        self,
        audience: Dict[str, Any],
        triggering_id: TRIGGERING_ID,
        entrance_id: Optional[str] = None,
        global_attributes: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """Enter an audience segment into a Sequence identified by
        ``triggering_id``. If multiple Sequences share a ``triggering_id``, the
        call enters audiences in all of them.

        :param audience: [required] An audience selector determining the set of
            channels to enter into the Sequence. Use the selectors in
            ``urbanairship`` (e.g. ``ua.tag``, ``ua.named_user``, ``ua.and_``,
            ``ua.or_``) to build this value.
        :param triggering_id: [required] The identifier of a Sequence's
            configured API Entrance trigger. May be a single string (1-256
            characters) or a list of 1 to 10 such strings.
        :param entrance_id: [optional] A unique identifier for enrolling the
            same users in multiple concurrent, independent instances of a
            Sequence. Each call with a different ``entrance_id`` creates a new
            enrollment without overwriting earlier ones. 1-64 characters.
        :param global_attributes: [optional] A dict of arbitrary keys and values
            used for personalization of triggered pushes. Top-level keys cannot
            start with the reserved prefix ``ua_``.
        :returns: API response dict.
        :raises urbanairship.AirshipFailure: for non-2xx API responses.
        :raises urbanairship.Unauthorized: for 401 responses.
        :raises urbanairship.ConnectionFailure: for connection errors.
        """
        body: Dict[str, Any] = {
            "audience": audience,
            "triggering_id": self._validate_triggering_id(triggering_id),
        }

        if entrance_id is not None:
            body["entrance_id"] = entrance_id
        if global_attributes is not None:
            body["global_attributes"] = global_attributes

        response = self.airship.request(
            method="POST",
            body=json.dumps(body),
            url=self.airship.urls.get("journeys_trigger_url"),
            content_type="application/json",
            version=3,
        )

        return cast(Dict[Any, Any], response.json())

    def exit(
        self,
        triggering_id: TRIGGERING_ID,
        entrance_id: Optional[str] = None,
    ) -> Dict:
        """Exit in-flight users from a Sequence identified by ``triggering_id``.
        This is a potentially long-running, asynchronous operation.

        :param triggering_id: [required] The identifier of a Sequence's
            configured API Entrance trigger. May be a single string (1-256
            characters) or a list of 1 to 10 such strings.
        :param entrance_id: [optional] Identifies a specific entrance for exit.
            If provided, only users that entered with this ``entrance_id`` are
            exited. If omitted, only users that entered without an
            ``entrance_id`` are exited. 1-64 characters.
        :returns: API response dict.
        :raises urbanairship.AirshipFailure: for non-2xx API responses.
        :raises urbanairship.Unauthorized: for 401 responses.
        :raises urbanairship.ConnectionFailure: for connection errors.
        """
        body: Dict[str, Any] = {
            "triggering_id": self._validate_triggering_id(triggering_id),
        }

        if entrance_id is not None:
            body["entrance_id"] = entrance_id

        response = self.airship.request(
            method="POST",
            body=json.dumps(body),
            url=self.airship.urls.get("journeys_exit_url"),
            content_type="application/json",
            version=3,
        )

        return cast(Dict[Any, Any], response.json())
