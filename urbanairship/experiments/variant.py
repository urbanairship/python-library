class Variant(object):
    """The variants for the experiment. An experiment must have at least 1 variant 
    and no more than 26.
    """

    def __init__(self,
                 description=None,
                 id,
                 name
                 ):
        """
        :keyword description: [optional] A description of the variant.
        :keyword id: [optional] Reflects the position of the variant in the array
            (beginning at 0). This ID is applied automatically and only appears
            in responses.
        :keyword name: [optional] A name for the variant.
        """
        self.description = description
        self.id = id
        self.name = name

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