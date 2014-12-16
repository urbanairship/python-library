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
    """Select a single Windows 8 APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid wns")
    return {"wns": uuid.lower().strip()}


def mpns(uuid):
    """Select a single Windows Phone 8 APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid mpns")
    return {"mpns": uuid.lower().strip()}


def tag(tag):
    """Select a single tag."""
    return {"tag": tag}


def alias(alias):
    """Select a single alias."""
    return {"alias": alias}


def segment(segment):
    """Select a single segment."""
    return {"segment": segment}


# Compound selectors


def or_(*children):
    """Select devices that match at least one of the given selectors.

    >>> or_(tag('sports'), tag('business'))
    {'or': [{'tag': 'sports'}, {'tag': 'business'}]}

    """
    return {"or": [child for child in children]}


def and_(*children):
    """Select devices that match all of the given selectors.

    >>> and_(tag('sports'), tag('business'))
    {'and': [{'tag': 'sports'}, {'tag': 'business'}]}

    """
    return {"and": [child for child in children]}

def not_(child):
    """Select devices that does not match the given selectors.

    >>> not_(and_(tag('sports'), tag('business')))
    {'not': {'and': [{'tag': 'sports'}, {'tag': 'business'}]}}

    """
    return {"not": child}


# Location selectors

def location(date=None, **kwargs):
    """Select a location expression.

    Location selectors are made up of either an id or an alias and a date
    period specifier. Use a date specification function to generate the time
    period specifier.

    ID location example:

    >>> from pprint import pprint
    >>> l = location(id='4oFkxX7RcUdirjtaenEQIV', date=recent_date(days=4))
    >>> pprint(l, width=76)
    {'location': {'date': {'recent': {'days': 4}},
                  'id': '4oFkxX7RcUdirjtaenEQIV'}}

    Alias location example:

    >>> l = location(us_zip='94103', date=absolute_date(
    ...    resolution='days', start='2012-01-01', end='2012-01-15'))
    >>> pprint(l, width=76)
    {'location': {'date': {'days': {'end': '2012-01-15',
                                    'start': '2012-01-01'}},
                  'us_zip': '94103'}}

    """
    if not len(kwargs) == 1:
        raise ValueError("Must specificy a single location id or alias")
    if date is None:
        raise ValueError("Must specificy a time period specifier")
    kwargs['date'] = date
    return {"location": kwargs}


def recent_date(last_seen=False, **kwargs):
    """Select a recent date range for a location selector.

    :keyword resolution: One keyword time resolution specifier, e.g. ``hours``
        or ``days``.
    :type resolution: int
    :keyword last_seen: Select only devices last seen in this location. Defaults
        to False.

    >>> recent_date(months=6)
    {'recent': {'months': 6}}
    >>> recent_date(weeks=3, last_seen=True)
    {'last_seen': True, 'recent': {'weeks': 3}}
    """
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
    """Select an absolute date range for a location selector.

    :keyword resolution: Time resolution specifier, e.g. ``hours`` or ``days``.
    :keyword start: UTC start time in ISO 8601 format.
    :keyword end: UTC end time in ISO 8601 format.
    :keyword last_seen: Select only devices last seen in this location.
        Defaults to False.

    >>> from pprint import pprint
    >>> d = absolute_date(resolution='months', start='2013-01', end='2013-06')
    >>> pprint(d)
    {'months': {'end': '2013-06', 'start': '2013-01'}}
    >>> d = absolute_date(resolution='minutes', start='2012-01-01 12:00',
    ...         end='2012-01-01 12:45', last_seen=True)
    >>> pprint(d, width=76)
    {'last_seen': True,
     'minutes': {'end': '2012-01-01 12:45', 'start': '2012-01-01 12:00'}}

    """
    if resolution not in ('minutes' 'hours' 'days' 'weeks' 'months' 'years'):
        raise ValueError("Invalid date resolution: %s" % resolution)

    payload = {resolution: {'start': start, 'end': end}}
    if last_seen:
        payload['last_seen'] = True
    return payload
