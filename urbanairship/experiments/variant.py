class Variant(object):
    """
    The variants for the experiment. An experiment must have at least 1 variant 
    and no more than 26.
    """

    def __init__(self,
                 description=None
                 ):
        """
        :keyword description: [optional] A description of the variant.
        """
        self.description = description

    @property
    def description(self, value):
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
