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
    device_types,
)

# Common selector for audience & device_types

all_ = "all"
