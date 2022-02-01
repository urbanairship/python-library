import re
from typing import Any, Dict, Optional, Union

DEVICE_TOKEN_FORMAT = re.compile(r"^[0-9a-fA-F]{64}$")
UUID_FORMAT = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}" r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
SMS_SENDER_FORMAT = re.compile(r"^[0-9]*$")
SMS_MSISDN_FORMAT = re.compile(r"^[0-9]*$")

# Value selectors; device IDs, aliases, tags, etc.
def ios_channel(uuid: str) -> Dict[str, str]:
    """Select a single iOS Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid iOS Channel")
    return {"ios_channel": uuid.lower().strip()}


def android_channel(uuid: str) -> Dict[str, str]:
    """Select a single Android Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid Android Channel")
    return {"android_channel": uuid.lower().strip()}


def amazon_channel(uuid: str) -> Dict[str, str]:
    """Select a single Amazon Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid Amazon Channel")
    return {"amazon_channel": uuid.lower().strip()}


def device_token(token: str) -> Dict[str, str]:
    """Select a single iOS device token"""
    # Ensure the device token is valid
    if not DEVICE_TOKEN_FORMAT.match(token):
        raise ValueError("Invalid device token")
    return {"device_token": token.upper().strip()}


def apid(uuid: str) -> Dict[str, str]:
    """Select a single Android APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid APID")
    return {"apid": uuid.lower().strip()}


def channel(uuid: str) -> Dict[str, str]:
    """Select a single channel.
    This selector may be used for any channel_id, regardless of device type"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid Channel")
    return {"channel": uuid.lower().strip()}


def open_channel(uuid: str) -> Dict[str, str]:
    """Select a single Open Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid Open Channel")
    return {"open_channel": uuid.lower().strip()}


def sms_sender(sender: str) -> Dict[str, str]:
    """Select an SMS Sender"""
    if not (isinstance(sender, str) or SMS_SENDER_FORMAT.match(sender)):
        raise ValueError("sms_sender value must be a numeric string.")
    return {"sms_sender": sender}


def sms_id(msisdn: str, sender: str) -> Dict[str, Dict]:
    """Select an SMS MSISDN"""
    if not (isinstance(msisdn, str) or SMS_MSISDN_FORMAT.match(msisdn)):
        raise ValueError("msisdn value must be a numeric string.")
    if not (isinstance(sender, str) or SMS_SENDER_FORMAT.match(sender)):
        raise ValueError("sender value must be a numeric string.")
    return {"sms_id": {"sender": sender, "msisdn": msisdn}}


def wns(uuid: str) -> Dict[str, str]:
    """Select a single Windows 8 APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid wns")
    return {"wns": uuid.lower().strip()}


def tag(tag: str) -> Dict[str, str]:
    """Select a single device tag."""
    return {"tag": tag}


def tag_group(tag_group: str, tag: str) -> Dict[str, str]:
    """Select a tag group and a tag."""
    payload = {"group": tag_group, "tag": tag}
    return payload


def alias(alias: str) -> Dict[str, str]:
    """Select a single alias."""
    return {"alias": alias}


def segment(segment: str) -> Dict[str, str]:
    """Select a single segment."""
    return {"segment": segment}


def named_user(name: str) -> Dict[str, str]:
    """Select a Named User ID"""
    return {"named_user": name}


def subscription_list(list_id: str) -> Dict[str, str]:
    """Select a subscription list"""
    return {"subscription_lists": list_id}


def static_list(list_id: str) -> Dict[str, str]:
    """Select a static list"""
    return {"static_list": list_id}


# Attribute selectors
def date_attribute(
    attribute: str,
    operator: str,
    precision: Optional[str] = None,
    value: Optional[Union[str, int]] = None,
) -> Dict[str, Any]:
    """
    Select an audience to send to based on an attribute object with a DATE schema type,
    including predefined and device attributes.
    Please refer to https://docs.airship.com/api/ua/?http#schemas-dateattribute for
    more information about using this selector, including information about required
    data formatting for values.
    Custom attributes must be defined in the Airship UI prior to use.
    """
    if operator not in ["is_empty", "before", "after", "range", "equals"]:
        raise ValueError(
            "operator must be one of: 'is_empty', 'before', 'after', 'range', 'equals'"
        )

    selector: Dict[str, Any] = {"attribute": attribute, "operator": operator}

    if operator == "range":
        if value is None:
            raise ValueError(
                "value must be included when using the '{0}' operator".format(operator)
            )

        selector["value"] = value

    if operator in ["before", "after", "equals"]:
        if value is None:
            raise ValueError(
                "value must be included when using the '{0}' operator".format(operator)
            )
        if precision is None:
            raise ValueError(
                "precision must be included when using the '{0}' operator".format(
                    operator
                )
            )

        selector["value"] = value
        selector["precision"] = precision

    return selector


def text_attribute(attribute: str, operator: str, value: str) -> Dict[str, Any]:
    """
    Select an audience to send to based on an attribute object with a TEXT schema type,
    including predefined and device attributes.

    Please refer to https://docs.airship.com/api/ua/?http#schemas-textattribute for
    more information about using this selector, including information about required
    data formatting for values.

    Custom attributes must be defined in the Airship UI prior to use.
    """
    if operator not in ["equals", "contains", "less", "greater", "is_empty"]:
        raise ValueError(
            "operator must be one of 'equals', 'contains', 'less', 'greater', 'is_empty'"
        )

    if type(value) is not str:
        raise ValueError("value must be a string")

    return {"attribute": attribute, "operator": operator, "value": value}


def number_attribute(attribute: str, operator: str, value: int) -> Dict[str, Any]:
    """
    Select an audience to send to based on an attribute object with a INTEGER schema
    type, including predefined and device attributes.

    Please refer to https://docs.airship.com/api/ua/?http#schemas-numberattribute for
    more information about using this selector, including information about required
    data formatting for values.

    Custom attributes must be defined in the Airship UI prior to use.
    """
    if operator not in ["equals", "contains", "less", "greater", "is_empty"]:
        raise ValueError(
            "operator must be one of 'equals', 'contains', 'less', 'greater', 'is_empty'"
        )

    if type(value) is not int:
        raise ValueError("value must be an integer")

    return {"attribute": attribute, "operator": operator, "value": value}


# Compound selectors
def or_(*children: Any) -> Dict[str, Any]:
    """Select devices that match at least one of the given selectors.

    >>> or_(tag('sports'), tag('business'))
    {'or': [{'tag': 'sports'}, {'tag': 'business'}]}

    """
    return {"or": [child for child in children]}


def and_(*children: Any) -> Dict[str, Any]:
    """Select devices that match all of the given selectors.

    >>> and_(tag('sports'), tag('business'))
    {'and': [{'tag': 'sports'}, {'tag': 'business'}]}

    """
    return {"and": [child for child in children]}


def not_(child: Any) -> Dict[str, Any]:
    """Select devices that does not match the given selectors.

    >>> not_(and_(tag('sports'), tag('business')))
    {'not': {'and': [{'tag': 'sports'}, {'tag': 'business'}]}}

    """
    return {"not": child}
