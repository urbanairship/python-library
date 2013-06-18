from .core import Push

from .audience import (
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
)

from .payload import (
    notification,
    ios,
    android,
    blackberry,
    wns_payload,
    mpns_payload,
    message,
    device_types,
)

# Common selector for audience & device_types

all_ = "all"
"""Select all, to do a broadcast.

Used in both ``audience`` and ``device_types``.
"""


__all__ = [
    all_,
    Push,
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
]
