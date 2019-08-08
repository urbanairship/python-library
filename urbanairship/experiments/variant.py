class Variant(object):
    """The variants for the experiment. An experiment must have at least 1 variant
    and no more than 26.
    """

    def __init__(self,
                 push,
                 description=None,
                 name=None,
                 campaigns=None,
                 in_app=None,
                 message=None,
                 notification=None,
                 options=None
                 ):
        # in the varient inside the PUSH: campaigns, in_app, message,
        # notification, options
        """

        :keyword push: [required] A push object without audience and device_types
            fields. These two fields are not allowed because they are already defined
            in the experiment object
        :keyword description: [optional] A description of the variant.
        :keyword name: [optional] A name for the variant
        :keyword campaings: [optional] An object specifying custom campaign categories
            related to the notification
        :keyword in_app: [optional] An object specifying custom campaign categories
            related to the notification.
        :keyword message: [optional] A Message Center message
        :keyword notification: [optional] The notification payload that is required
            unless either message or in_app is present. You can provide an alert and any
            platform overrides that apply to the device_type platforms you specify.
        :keyword options: [optional] A JSON dictionary for specifying non-payload
            options related to the delivery of the push

        """
        self.push = push
        self.description = description
        self.name = name
        self.campaings = campaings
        self.in_app = in_app
        self.message = message
        self.notification = notification
        self.options = options

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
