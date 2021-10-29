class Variant(object):
    """The variants for the experiment. An experiment must have at least 1 variant
    and no more than 26.
    """

    def __init__(self, push, description=None, name=None, schedule=None, weight=None):
        """
        :keyword push: [required] A push object without audience and device_types
            fields. These two fields are not allowed because they are already defined
            in the experiment object
        :keyword description: [optional] A description of the variant.
        :keyword name: [optional] A name for the variant
            unless either message or in_app is present. You can provide an alert and any
            platform overrides that apply to the device_type platforms you specify.
        :keyword schedule: [optional] The time when the push notification should be sent
        :keyword weight: [optional] The proportion of the audience that will receive
            this variant. Defaults to 1.
        """
        self.push = push
        self.description = description
        self.name = name
        self.schedule = schedule
        self.weight = weight

    @property
    def description(self):
        if not self._description:
            return None
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            TypeError("the description must be type string")

        self._description = value

    @property
    def name(self):
        if not self._name:
            return None
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            TypeError("the name must be a string type")

        self._name = value

    @property
    def weight(self):
        if not self._weight:
            return None
        return self._weight

    @weight.setter
    def weight(self, value):
        if not isinstance(value, int):
            TypeError("the value must be a integer type")
        self._weight = value
