class Experiment(object):
    """ An experiment object describes an A/B test,
    including the audience and variant portions.
    """

    def __init__(self,
                 name=None):
        """
        :keyword name: [optional] A name for the experiment
        """
        self.name = name

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
