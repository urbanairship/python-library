class Variant(object):
    """The variants for the experiment. An experiment must have at least 1 variant
    and no more than 26.
    """

    def __init__(self,
                 push,
                 description=None,
                 id=None,
                 name=None,
                 schedule=None,
                 weight=None
                 ):
        """
        :keyword description: [optional] A description of the variant.
        :keyword id: [optional] Reflects the position of the variant in the array
            (beginning at 0). This ID is applied automatically and only appears
            in responses
        :keyword name: [optional] A name for the variant
        :keyword push: [required] A push object without audience and device_types
            fields. These two fields are not allowed because they are already defined
            in the experiment object
        :keyword schedule: [optional] The time when the push notification should be sent
        :keyword weight: [optional] The proportion of the audience that will receive
            this variant. Defaults to 1.
        """
        self.description = description
        self.id = id
        self.name = name
        self.push = push
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
            TypeError(
                'the description must be type string'
            )

        self._description = value

    @property
    def id(self):
        if not self._id:
            return None
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            TypeError(
                'the description must be type integer'
            )

        self._id = value

    @property
    def name(self):
        if not self._name:
            return None
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            TypeError(
                'the name must be a string type'
            )

        self._name = value

    @property
    def weight(self):
        if not self._weight:
            return None
        return self._weight

    @weight.setter
    def weight(self, value):
        if not isinstance(value, int):
            TypeError(
                'the name must be a integer type'
            )
        self._weight = value
