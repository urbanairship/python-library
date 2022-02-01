from typing import Any, List, Optional, Dict, Union


class Pipeline(object):
    """
    Pipeline object encapsulates the complete set of objects that define an Automation
    pipeline
    """

    def __init__(
        self,
        enabled: Optional[bool] = None,
        name: Optional[str] = None,
        historical_trigger: Optional[Dict] = None,
        timing: Optional[Dict] = None,
        immediate_trigger: Optional[Union[Dict, List]] = None,
        cancellation_trigger: Optional[Union[Dict, List]] = None,
        constraint: Optional[Union[Dict, List]] = None,
        condition: Optional[Union[Dict, List]] = None,
        outcome: Optional[Union[Dict, List]] = None,
    ) -> None:
        """Create Pipeline object for Automation payload

        :keyword enabled: boolean value determines active status of the pipeline
        :keyword outcome: a push object to be sent as outcome of the pipeline
        :keyword name: [optional] descriptive string for pipeline identification
        :keyword immediate_trigger: [optional] single event identifier or list
            of event identifiers that trigger the outcome of the pipeline -
            trigger list can be combination of simple and compound identifiers
        :keyword cancellation_trigger: [optional] single event identifier or
            list of event identifiers that trigger cancellation of the pipeline
            outcome - can be combination of simple and compound identifiers
        :keyword historical_trigger: [optional] single or list of historical
            trigger objects that currently match only inactive triggers
        :keyword constraint: [optional] single or list of constraint objects
            that limit the number of pushes sent to a device in a given time
            period
        :keyword condition: [optional] one or a list of condition sets with an
            and/or operator for combining the conditions
        :keyword timing: [optional] a timing object defining times allowable
            for outcome delivery
        """
        self.enabled = enabled
        self.outcome = outcome
        self.name = name
        self.immediate_trigger = immediate_trigger
        self.cancellation_trigger = cancellation_trigger
        self.historical_trigger = historical_trigger
        self.constraint = constraint
        self.condition = condition
        self.timing = timing

    @property
    def payload(self) -> Dict:
        """JSON serialized Pipeline object"""
        if not isinstance(self.enabled, bool):
            raise TypeError("enabled is required and must be a boolean value")
        if not self.outcome:
            raise ValueError("outcome is required for automation pipelines")

        data: Dict[str, Any] = {"enabled": self.enabled, "outcome": self.outcome}

        if self.name is not None:
            data["name"] = self.name
        if self.immediate_trigger is not None:
            data["immediate_trigger"] = self.immediate_trigger
        if self.cancellation_trigger is not None:
            data["cancellation_trigger"] = self.cancellation_trigger
        if self.historical_trigger is not None:
            data["historical_trigger"] = self.historical_trigger
        if self.constraint is not None:
            data["constraint"] = self.constraint
        if self.condition is not None:
            data["condition"] = self.condition
        if self.timing is not None:
            data["timing"] = self.timing

        return data

    def from_dict(self, pipeline_dict: Dict) -> None:
        for k in pipeline_dict:
            setattr(self, k, pipeline_dict[k])

    @property
    def outcome(self) -> Optional[Union[List, Dict]]:
        if not self._outcomes:
            return None
        if len(self._outcomes) == 1:
            return self._outcomes[0]

        return self._outcomes

    @outcome.setter
    def outcome(self, outcome_object: Optional[Union[Dict, List]]) -> None:
        """Set outcome object

        :keyword outcome_object: Single outcome object or list of outcome objects.
            Outcomes are push objects.

        """
        if outcome_object is None:
            self._outcomes = []
        elif isinstance(outcome_object, list):
            to_set = []
            for push in outcome_object:
                if "push" in push:
                    to_set.append(push)
                else:
                    to_set.append({"push": push})
            self._outcomes = to_set
        elif isinstance(outcome_object, dict):
            if "push" in outcome_object:
                self._outcomes = [outcome_object]
            else:
                self._outcomes = [{"push": outcome_object}]
        else:
            raise TypeError("outcome must be outcome object or list of outcome objects")

    def append_outcome_object(self, push_object: Dict) -> None:
        """Append outcome object to current Pipeline outcome

        :keyword push_object: A push object that will be an outcome for this Pipeline
            object

        """
        if not isinstance(push_object, dict):
            TypeError("outcome object requires a push object as a dictionary")

        to_append = {}
        if isinstance(push_object, dict):
            to_append = push_object

        self._outcomes.append(to_append)

    def remove_outcome_object(self, push_object: Dict) -> None:
        """Remove outcome push object from current outcome

        :keyword push_object: A push object to remove from the outcome of this Pipeline
            object

        """
        self._outcomes.remove(push_object)

    @property
    def immediate_trigger(self) -> Optional[Union[Dict, List]]:
        if not self._immediate_trigger:
            return None
        if len(self._immediate_trigger) == 1:
            return self._immediate_trigger[0]

        return self._immediate_trigger

    @immediate_trigger.setter
    def immediate_trigger(self, event_identifiers: Optional[Union[Dict, List]]) -> None:
        """Set immediate trigger for Pipeline

        :keyword event_identifiers: One or list of event identifiers

        """
        if event_identifiers:
            if not isinstance(event_identifiers, (dict, list)):
                TypeError(
                    "immediate trigger must be an event identifier dictionary "
                    "or list of event identifier dictionaries"
                )

            if isinstance(event_identifiers, list):
                self._immediate_trigger = event_identifiers

            if isinstance(event_identifiers, dict):
                self._immediate_trigger = [event_identifiers]
        else:
            self._immediate_trigger = []

    def append_immediate_trigger_identifier(self, event_identifier: Dict) -> None:
        """Append event identifier to immediate triggers for Pipeline

        :keyword event_identifier: Event identifier object

        """
        self._immediate_trigger.append(event_identifier)

    def remove_immediate_trigger_identifier(self, event_identifier: Dict) -> None:
        """Remove event identifier to immediate triggers for Pipeline

        :keyword event_identifier: Even identifier object

        """
        self._immediate_trigger.remove(event_identifier)

    @property
    def cancellation_trigger(self) -> Optional[Union[Dict, List]]:
        if not self._cancellation_trigger:
            return None
        if len(self._cancellation_trigger) == 1:
            return self._cancellation_trigger[0]

        return self._cancellation_trigger

    @cancellation_trigger.setter
    def cancellation_trigger(
        self, event_identifiers: Optional[Union[Dict, List]]
    ) -> None:
        """Set Pipeline cancellation trigger

        :keyword event_identifiers: One of list of event identifiers

        """
        if event_identifiers:
            if not isinstance(event_identifiers, (str, dict, list)):
                TypeError(
                    "immediate trigger must be an event identifier or "
                    "list of event identifiers"
                )

            if isinstance(event_identifiers, list):
                self._cancellation_trigger = event_identifiers
            else:
                self._cancellation_trigger = [event_identifiers]
        else:
            self._cancellation_trigger = []

    def append_cancellation_trigger_identifier(self, event_identifier: Dict) -> None:
        """Append event identifier to immediate triggers for Pipeline

        :keyword event_identifier: Event identifier object
        """
        self._cancellation_trigger.append(event_identifier)

    def remove_cancellation_trigger_identifier(self, event_identifier: Dict) -> None:
        """Remove event identifier from immediate triggers for Pipeline

        :keyword event_identifier: Event identifier object

        """
        self._cancellation_trigger.remove(event_identifier)

    @property
    def historical_trigger(self) -> Optional[Dict]:
        return self._historical_trigger

    @historical_trigger.setter
    def historical_trigger(self, historical_trigger_object: Optional[Dict]) -> None:
        """Set historical trigger for Pipeline

        :keyword historical_trigger_object: Historical trigger object for
            triggering Pipeline outcome

        """
        if historical_trigger_object:
            if historical_trigger_object["event"] != "open":
                raise ValueError(
                    'only allowable value of historical trigger "event" is "open"'
                )

            if historical_trigger_object["equals"] != 0:
                raise ValueError(
                    'only allowable value of historial trigger "equals" is 0'
                )

            if 0 >= historical_trigger_object["days"] > 90:
                raise ValueError("days of inactivity must be between 1 and 90")

        self._historical_trigger = historical_trigger_object

    @property
    def constraint(self) -> Optional[Union[Dict, List]]:
        if not self._constraints:
            return None
        if len(self._constraints) == 1:
            return self._constraints[0]

        return self._constraints

    @constraint.setter
    def constraint(self, constraint_objects: Union[Dict, List]) -> None:
        """Set Pipline constraints

        :keyword constraint_objects: One of list of constraint objects
        """
        if constraint_objects:
            if not isinstance(constraint_objects, (dict, list)):
                TypeError(
                    "constraint must be single constraint object or list of constraint objects"
                )

            if isinstance(constraint_objects, list):
                self._constraints = constraint_objects
            if isinstance(constraint_objects, dict):
                self._constraints = [constraint_objects]
        else:
            self._constraints = []

    def append_constraint_object(self, constraint_object: Dict) -> None:
        """Append constraint object to constraint for Pipeline

        :keyword constraint_object: Constraint object to append to Pipeline constraint

        """
        if not isinstance(constraint_object, dict):
            TypeError("a single constraint object must be a dictionary")

        self._constraints.append(constraint_object)

    def remove_constraint_object(self, constraint_object: Dict) -> None:
        self._constraints.remove(constraint_object)

    @property
    def condition(self) -> Optional[Union[Dict, List]]:
        if not self._condition_sets:
            return None
        if len(self._condition_sets) == 1:
            return self._condition_sets[0]

        return self._condition_sets

    @condition.setter
    def condition(self, condition_sets: Union[List, Dict]) -> None:
        """Set condition for Pipeline

        :keyword condition_sets: One or list of condition sets

        """
        if condition_sets:
            if not isinstance(condition_sets, (list, dict)):
                raise TypeError(
                    "condition_sets must be a condition set "
                    "or list of condition sets"
                )

            if isinstance(condition_sets, list):
                if len(condition_sets) > 20:
                    raise ValueError("condition maximum is 20 condition sets")

            if self._validate_condition_set(condition_sets):
                if isinstance(condition_sets, list):
                    self._condition_sets = condition_sets
                else:
                    self._condition_sets = [condition_sets]
        else:
            self._condition_sets = []

    def append_condition_set(self, condition_set: Dict) -> None:
        """Append condition set to Pipeline condition

        :keyword condition_set: One or list of condition sets

        """
        if not isinstance(condition_set, dict):
            TypeError("a single condition set object must be a dictionary")

        if self._validate_condition_set(condition_set):
            self._condition_sets.append(condition_set)

    def remove_condition_set(self, condition_set: Dict) -> None:
        """Remove condition set from Pipeline condition

        :keyword condition_set: One or list of condition sets

        """
        self._condition_sets.remove(condition_set)

    def _validate_condition_set(self, condition_sets: Union[Dict, List]) -> bool:
        invalid_operators = []
        if isinstance(condition_sets, list):
            for condition_set in condition_sets:
                for operator in condition_set:
                    if operator not in ["and", "or"]:
                        invalid_operators.append(operator)
        else:
            for operator in condition_sets:
                if operator not in ["and", "or"]:
                    invalid_operators.append(operator)

        if invalid_operators:
            raise KeyError(
                'invalid operators: {}, must be "and" or "or"'.format(
                    ", ".join(invalid_operators)
                )
            )

        return True

    @property
    def timing(self) -> Optional[Dict]:
        return self._timing

    @timing.setter
    def timing(self, timing_object: Optional[Dict]) -> None:
        """Set timing object for available send times for Pipeline

        :keyword timing_object: Single timing object defining allowable
        delivery times for Pipeline

        """
        if timing_object:
            if "delay" in timing_object:
                delay = timing_object["delay"]["seconds"]

                if not (isinstance(delay, int) and delay > 0):
                    raise ValueError("delay must be an integer greater than 0")

            if "schedule" in timing_object:
                schedule = timing_object["schedule"]
                if "type" not in schedule:
                    raise KeyError('"type" is required for a timing schedule')
                if not schedule["type"] in ("local", "utc"):
                    raise ValueError('timing schedule "type" must be "local" or "utc"')

                if "dayparts" not in schedule:
                    raise KeyError('"dayparts" is required for a timing schedule')

            self._timing: Optional[Dict] = timing_object
        else:
            self._timing = None

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value
