"""Python package for using the Urban Airship API"""
from .core import Airship
from .common import AirshipFailure, Unauthorized
from .push import (
    Push,
    ScheduledPush,
    all_,
    device_token,
    device_pin,
    apid,
    wns,
    mpns,
    tag,
    alias,
    segment,
    and_,
    or_,
    not_,
    location,
    recent_date,
    absolute_date,
    notification,
    ios,
    android,
    blackberry,
    wns_payload,
    mpns_payload,
    message,
    device_types,
    scheduled_time,
)
from .devices import (
    DeviceTokenList,
    DevicePINList,
    APIDList,
)


__all__ = [
    Airship,
    AirshipFailure,
    Unauthorized,
    all_,
    Push,
    ScheduledPush,
    device_token,
    device_pin,
    apid,
    wns,
    mpns,
    tag,
    alias,
    segment,
    and_,
    or_,
    not_,
    location,
    recent_date,
    absolute_date,
    notification,
    ios,
    android,
    blackberry,
    wns_payload,
    mpns_payload,
    message,
    device_types,
    scheduled_time,
    DeviceTokenList,
    DevicePINList,
    APIDList,
]

# Silence urllib3 INFO logging by default

import logging
logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
