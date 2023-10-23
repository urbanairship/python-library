from enum import Enum


class LiveActivityEvent(Enum):
    UPDATE = "update"
    END = "end"


class LiveUpdateEvent(Enum):
    START = "start"
    UPDATE = "update"
    END = "end"
