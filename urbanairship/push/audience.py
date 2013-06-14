import re

DEVICE_TOKEN_FORMAT = re.compile(r'^[0-9a-fA-F]{64}$')
PIN_FORMAT = re.compile(r'^[0-9a-fA-F]{8}$')
UUID_FORMAT = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}'
    r'-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


# Value selectors; device IDs, aliases, tags, etc.


def device_token(token):
    """Select a single iOS device token"""
    # Ensure the device token is valid
    if not DEVICE_TOKEN_FORMAT.match(token):
        raise ValueError("Invalid device token")
    return {"device_token": token.upper().strip()}


def device_pin(pin):
    """Select a single BlackBerry PIN"""
    if not PIN_FORMAT.match(pin):
        raise ValueError("Invalid BlackBerry PIN")
    return {"device_pin": pin.lower().strip()}


def apid(uuid):
    """Select a single Android APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid APID")
    return {"apid": uuid.lower().strip()}


def wns(uuid):
    """Select a single Windows 8 apid"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid wns")
    return {"wns": uuid.lower().strip()}


def mpns(uuid):
    """Select a single Windows 8 Phone apid"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid mpns")
    return {"mpns": uuid.lower().strip()}


def tag(tag):
    return {"tag": tag}


def alias(alias):
    return {"alias": alias}


def segment(segment):
    return {"segment": segment}


# Compound selectors


def or_(*children):
    return {"or": [child for child in children]}


def and_(*children):
    return {"and": [child for child in children]}

def not_(child):
    return {"not": child}


# Location selectors

def location(date=None, **kwargs):
    """Select a location expression.

    Location selectors are made up of either an id or an alias and a date
    period specifier. Use a date specification function to generate the time
    period specifier.

    Examples:
    >>> location(id='4oFkxX7RcUdirjtaenEQIV', date=recent_date(days=4)
    >>> location(us_zip='94103', date=absolute_date(
        resolution='days', start='2012-01-01', end='2012-01-15')
    """

    if not len(kwargs) == 1:
        raise ValueError("Must specificy a single location id or alias")
    if date is None:
        raise ValueError("Must specificy a time period specifier")
    kwargs['date'] = date
    return {"location": kwargs}


def recent_date(last_seen=False, **kwargs):
    if not len(kwargs) == 1:
        raise ValueError("Must specificy a single date resolution")
    resolution = kwargs.keys()[0]
    value = kwargs.values()[0]

    if resolution not in ('minutes' 'hours' 'days' 'weeks' 'months' 'years'):
        raise ValueError("Invalid date resolution: %s" % resolution)
    payload = {"recent": {resolution: value}}
    if last_seen:
        payload['last_seen'] = True
    return payload


def absolute_date(resolution, start, end, last_seen=False):
    if resolution not in ('minutes' 'hours' 'days' 'weeks' 'months' 'years'):
        raise ValueError("Invalid date resolution: %s" % resolution)

    payload = {resolution: {'start': start, 'end': end}}
    if last_seen:
        payload['last_seen'] = True
    return payload
