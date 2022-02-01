from typing import Dict, Any, Optional, List

from urbanairship.experiments.variant import Variant


class Experiment(object):
    """An experiment object describes an A/B test,
    including the audience and variant portions.
    """

    def __init__(
        self,
        audience: Dict[str, Any],
        device_types: List[str],
        variants: List[Variant],
        name: Optional[str] = None,
        description: Optional[str] = None,
        weight: Optional[int] = None,
        campaigns: Optional[Dict[str, Any]] = None,
        control: Optional[float] = None,
    ) -> None:
        """
        :keyword audience: [required] The audience for the experiment
        :keyword device_types: A list containing one or more strings identifying
            targeted platforms. Accepted platforms are ios, android, amazon, wns, web,
            sms, email, and open::<open_platform_name>
        :keyword variants: [required] The variants for the experiment. An experiment
            must have at least 1 variant and no more than 26.
        :keyword name: [optional] A name for the experiment
        :keyword description: [optional] A description of the experiment
        :keyword campaigns: [optional] Campaigns object that will be applied to
            resulting pushes
        :keyword control: [optional] The proportional subset of the audience that will
             not receive a push

        """
        self.audience = audience
        self.device_types = device_types
        self.variants = variants
        self.name = name
        self.description = description
        self.campaigns = campaigns
        self.control = control
        self.weight = weight

    @property
    def payload(self) -> Dict[str, Any]:
        """JSON serialized experiment object"""

        variants_data: List = []
        for variant in self.variants:
            variant_data: Dict[str, Any] = {}
            push_options: Dict[str, Any] = {}

            if getattr(variant, "description", None):
                variant_data["description"] = variant.description
            if getattr(variant, "name", None):
                variant_data["name"] = variant.name

            if getattr(variant.push, "in_app", None):
                push_options["in_app"] = variant.push.in_app
            if getattr(variant.push, "notification", None):
                push_options["notification"] = variant.push.notification
            if getattr(variant.push, "options", None):
                push_options["options"] = variant.push.options
            if getattr(variant, "schedule", None):
                variant_data["schedule"] = variant.schedule
            if getattr(variant, "weight", None):
                variant_data["weight"] = variant.weight

            variant_data["push"] = push_options
            variants_data.append(variant_data)

        data: Dict[str, Any] = {
            "audience": self.audience,
            "device_types": self.device_types,
            "variants": variants_data,
        }

        if self.name is not None:
            data["name"] = self.name
        if self.description is not None:
            data["description"] = self.description
        if self.campaigns is not None:
            data["campaigns"] = self.campaigns
        if self.control is not None:
            data["control"] = self.control

        if self.weight is not None:
            variant_data["weight"] = self.weight

        return data

    @property
    def name(self) -> Optional[str]:
        if not self._name:
            return None
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        if not isinstance(value, str):
            TypeError("the name must be a string type")

        self._name = value

    @property
    def description(self) -> Optional[str]:
        if not self._description:
            return None
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        if not isinstance(value, str):
            TypeError("the description must be type string")

        self._description = value

    @property
    def control(self) -> Optional[float]:
        if not self._control:
            return None
        return self._control

    @control.setter
    def control(self, value: Optional[float]) -> None:
        if not isinstance(value, float):
            TypeError("the control must be type float")
        if value is not None:
            if not 0.0 >= value >= 1.0:
                ValueError("control must be in a range of 0.0 and 1.0")

        self._control = value
