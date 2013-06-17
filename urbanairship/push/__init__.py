from .delivery import Push

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

from .message import (
    notification,
    ios,
    android,
    blackberry,
    wns_payload,
    mpns_payload,
    device_types,
)

# Common selector for audience & device_types

#: Select all, to do a broadcast.
#: Used in both ``audience`` and ``device_types``.
all_ = "all"
