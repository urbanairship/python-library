class Experiment(object):
    """ An experiment object describes an A/B test,
    including the audience and variant portions.
    """

    def __init__(self,
                 audience,
                 device_types,
                 name=None,
                 description=None,
                 campaigns=None,
                 control=None
                 ):
        """
        :keyword audience: [required] The audience for the experiment
        :keyword device_types: An array containing one or more strings identifying
            targeted platforms. Accepted platforms are ios, android, amazon, wns, web,
            sms, email, and open::<open_platform_name>
        :keyword name: [optional] A name for the experiment
        :keyword description: [optional] A description of the experiment
        :keyword campaigns: [optional] Campaigns object that will be applied to
            resulting pushes
        :keyword control: [optional] The proportional subset of the audience that will
             not receive a push
        """
        self.audience = audience
        self.device_types = device_types
        self.name = name
        self.description = description
        self.campaigns = campaigns
        self.control = control

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
    def control(self):
        if not self._control:
            return None
        return self._control

    @control.setter
    def control(self, value):
        if not isinstance(value, float):
            TypeError(
                'the control must be type float'
            )
        if not 0.0 >= value >= 1.0:
            ValueError(
                'control must be in a range of 0.0 and 1.0'
            )
        self._control = value
