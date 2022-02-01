import datetime
from typing import Dict, Optional, Union
import json

from urbanairship import Airship


class CustomEvent:
    def __init__(
        self,
        airship: Airship,
        name: str,
        user: Dict,
        interaction_type: Optional[str] = None,
        interaction_id: Optional[str] = None,
        properties: Optional[Dict] = None,
        session_id: Optional[str] = None,
        transaction: Optional[str] = None,
        value: Optional[Union[int, float]] = None,
        occurred: Optional[datetime.datetime] = None,
    ) -> None:
        """
        A class representing an Airship custom event. Please see the
        documentation at https://docs.airship.com/api/ua/?http#tag-custom-events for
        details on Custom Event usage.

        :param Airship: [required] An urbanairship.Airship instance initialized with
            bearer token authentication.
        :param name: [required] A plain-text name for the event. Airship's analytics
            systems will roll up events with the same name, providing counts and total
            value associated with the event. This value cannot contain upper-case
            characters. If the name contains upper-case characters, you will receive a
            400 response.
        :param user: [required] An Airship channel identifier or named user
            for the user who triggered the event.
        :param interaction_id: [optional] The identifier defining where the event
            occurred.
        :param interaction_type: [optional] Describes the type of interaction that
            triggered the event
        :param properties: [optional] A dict containing custom event properties.
        :param session_id: [optional] The user session during which the event occurred.
            You must supply and maintain session identifiers.
        :param transaction: [optional] If the event is one in a series representing a
            single transaction, use the transaction field to tie events together.
        :param value: [optional] If the event is associated with a count or amount,
            the 'value' field carries that information.
        :param occurred: [optional] The date and time when the event occurred. Events
            must have occurred within the past 90 days. You cannot provide
            a future datetime.
        """
        self.airship = airship
        self.name = name
        self.user = user
        self.interaction_type = interaction_type
        self.interaction_id = interaction_id
        self.properties = properties
        self.session_id = session_id
        self.transaction = transaction
        self.value = value
        self.occurred = occurred

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def user(self) -> Dict:
        if "named_user" in self._user.keys():
            return {"named_user_id": self._user["named_user"]}

        return self._user

    @user.setter
    def user(self, value: Dict) -> None:
        self._user = value

    @property
    def interaction_id(self) -> Optional[str]:
        return self._interaction_id

    @interaction_id.setter
    def interaction_id(self, value: str) -> None:
        self._interaction_id = value

    @property
    def interaction_type(self) -> Optional[str]:
        return self._interaction_type

    @interaction_type.setter
    def interaction_type(self, value: str) -> None:
        self._interaction_type = value

    @property
    def properties(self) -> Optional[Dict]:
        return self._properties

    @properties.setter
    def properties(self, value: Optional[Dict]) -> None:
        self._properties = value

    @property
    def session_id(self) -> Optional[str]:
        return self._session_id

    @session_id.setter
    def session_id(self, value: Optional[str]) -> None:
        self._session_id = value

    @property
    def transaction(self) -> Optional[str]:
        return self._transaction

    @transaction.setter
    def transaction(self, value: Optional[str]) -> None:
        self._transaction = value

    @property
    def value(self) -> Optional[Union[int, float]]:
        return self._value

    @value.setter
    def value(self, value: Optional[Union[int, float]]):
        self._value = value

    @property
    def occurred(self) -> Optional[datetime.datetime]:
        return self._occurred

    @occurred.setter
    def occurred(self, value: Optional[datetime.datetime]) -> None:
        self._occurred = value

    @property
    def _payload(self) -> Dict:
        event_payload: Dict = {"user": self.user}
        body: Dict = {"name": self.name}

        for payload_attr in ["occurred"]:
            if getattr(self, payload_attr) is not None:
                event_payload[payload_attr] = getattr(self, payload_attr).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                )

        for body_attr in [
            "value",
            "transaction",
            "interaction_id",
            "interaction_type",
            "properties",
            "session_id",
        ]:
            if getattr(self, body_attr) is not None:
                body[body_attr] = getattr(self, body_attr)

        event_payload["body"] = body

        return event_payload

    def send(self) -> Dict:
        """Send the Custom Event to Airship systems

        :returns: API response dict
        """
        response = self.airship.request(
            method="POST",
            body=json.dumps(self._payload),
            url=self.airship.urls.get("custom_events_url"),
            content_type="application/json",
            version=3,
        )

        return response.json()
