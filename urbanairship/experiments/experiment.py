class Experiment(object):
    """ An experiment object describes an A/B test,
    including the audience and variant portions.
    """

    def __init__(self,
                 audience,
                 device_types,
                 variants,
                 push,
                 name=None,
                 description=None,
                 campaigns=None,
                 control=None,
                 in_app=None,
                 message=None,
                 notification=None,
                 options=None
                 ):
        """
        :keyword audience: [required] The audience for the experiment
        :keyword device_types: An array containing one or more strings identifying
            targeted platforms. Accepted platforms are ios, android, amazon, wns, web,
            sms, email, and open::<open_platform_name>
        :keywors variants: [required] The variants for the experiment. An experiment
            must have at least 1 variant and no more than 26.
        :keyword name: [optional] A name for the experiment
        :keyword description: [optional] A description of the experiment
        :keyword campaigns: [optional] Campaigns object that will be applied to
            resulting pushes
        :keyword control: [optional] The proportional subset of the audience that will
             not receive a push
        :keyword push: [optional] A push object without audience and device_types
            fields. These two fields are not allowed because they are already defined
            in the experiment object
        :keyword in_app: [optional] An object specifying custom campaign categories
            related to the notification.
        :keyword message: [optional] A Message Center message
        :keyword notification: [optional] The notification payload that is required
            unless either message or in_app is present. You can provide an alert and any
            platform overrides that apply to the device_type platforms you specify.
        :keyword options: [optional] A JSON dictionary for specifying non-payload
            options related to the delivery of the push
        """
        self.audience = audience
        self.device_types = device_types
        self.variants = variants
        self.name = name
        self.description = description
        self.campaigns = campaigns
        self.control = control
        self.push = push
        self.in_app = in_app
        self.message = message
        self.notification = notification
        self.options = options

    @property
    def payload(self):
        """JSON serialized experiment object"""

        variants_data = []
        for variant in self.variants:
            variant_data = {}

            if getattr(variant.description):
                variant_data['descriptinon'] = variant.description
            if getattr(variant.name):
                variant_data['name'] = variant.name
            if getattr(variant.schedule):
                variant_data['schedule'] = variant.schedule
            if getattr(variant.weight):
                variant_data['weight'] = variant.weight

            if getattr(variant.push.campaigns):
                variant_data['push']['campaigns'] = variant.push.campaigns
            if getattr(variant.push.in_app):
                variant_data['push']['in_app'] = variant.push.in_app
            if getattr(variant.push.notification):
                variant_data['push']['notification'] = variant.push.notification
            if getattr(variant.push.options):
                variant_data['push']['options'] = variant.push.options

        variants_data.append(variant_data)

        data = {
            "audiance": self.audience,
            "device_types": self.device_types,
            "variant": variants_data
        }

        return data

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
