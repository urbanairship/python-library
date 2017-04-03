import re

DEVICE_TOKEN_FORMAT = re.compile(r'^[0-9a-fA-F]{64}$')
UUID_FORMAT = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}'
    r'-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')


# Value selectors; device IDs, aliases, tags, etc.


def ios_channel(uuid):
    """Select a single iOS Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError('Invalid iOS Channel')
    return {'ios_channel': uuid.lower().strip()}


def android_channel(uuid):
    """Select a single Android Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError('Invalid Android Channel')
    return {'android_channel': uuid.lower().strip()}


def amazon_channel(uuid):
    """Select a single Amazon Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError('Invalid Amazon Channel')
    return {'amazon_channel': uuid.lower().strip()}


def device_token(token):
    """Select a single iOS device token"""
    # Ensure the device token is valid
    if not DEVICE_TOKEN_FORMAT.match(token):
        raise ValueError('Invalid device token')
    return {'device_token': token.upper().strip()}


def apid(uuid):
    """Select a single Android APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError('Invalid APID')
    return {'apid': uuid.lower().strip()}


def channel(uuid):
    """Select a single Web Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError('Invalid Channel')
    return {'channel': uuid.lower().strip()}


def wns(uuid):
    """Select a single Windows 8 APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError('Invalid wns')
    return {'wns': uuid.lower().strip()}


def tag(tag):
    """Select a single tag."""
    return {'tag': tag}


def alias(alias):
    """Select a single alias."""
    return {'alias': alias}


def segment(segment):
    """Select a single segment."""
    return {'segment': segment}


# Compound selectors


def or_(*children):
    """Select devices that match at least one of the given selectors.

    >>> or_(tag('sports'), tag('business'))
    {'or': [{'tag': 'sports'}, {'tag': 'business'}]}

    """
    return {'or': [child for child in children]}


def and_(*children):
    """Select devices that match all of the given selectors.

    >>> and_(tag('sports'), tag('business'))
    {'and': [{'tag': 'sports'}, {'tag': 'business'}]}

    """
    return {'and': [child for child in children]}


def not_(child):
    """Select devices that does not match the given selectors.

    >>> not_(and_(tag('sports'), tag('business')))
    {'not': {'and': [{'tag': 'sports'}, {'tag': 'business'}]}}

    """
    return {'not': child}


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
        raise ValueError('Must specify a single location id or alias')
    if date is None:
        raise ValueError('Must specify a time period specifier')
    kwargs['date'] = date
    return {'location': kwargs}


def recent_date(**kwargs):
    """Select a recent date range for a location selector.

    :keyword resolution: One keyword time resolution specifier, e.g. ``hours``
        or ``days``.
    :type resolution: int

    >>> recent_date(months=6)
    {'recent': {'months': 6}}
    >>> recent_date(weeks=3)
    {'recent': {'weeks': 3}}
    """
    if not len(kwargs) == 1:
        raise ValueError('Must specify a single date resolution')
    resolution = list(kwargs.keys())[0]
    value = list(kwargs.values())[0]

    if resolution not in ('minutes' 'hours' 'days' 'weeks' 'months' 'years'):
        raise ValueError('Invalid date resolution: %s' % resolution)
    payload = {'recent': {resolution: value}}
    return payload


def absolute_date(resolution, start, end):
    """Select an absolute date range for a location selector.

    :keyword resolution: Time resolution specifier, e.g. ``hours`` or ``days``.
    :keyword start: UTC start time in ISO 8601 format.
    :keyword end: UTC end time in ISO 8601 format.

    >>> from pprint import pprint
    >>> d = absolute_date(resolution='months', start='2013-01', end='2013-06')
    >>> pprint(d)
    {'months': {'end': '2013-06', 'start': '2013-01'}}
    >>> d = absolute_date(resolution='minutes', start='2012-01-01 12:00',
    ...         end='2012-01-01 12:45')
    >>> pprint(d, width=76)
    {'minutes': {'end': '2012-01-01 12:45', 'start': '2012-01-01 12:00'}}

    """
    if resolution not in ('minutes' 'hours' 'days' 'weeks' 'months' 'years'):
        raise ValueError('Invalid date resolution: %s' % resolution)

    payload = {resolution: {'start': start, 'end': end}}
    return payload


def named_user(name):
    return {'named_user': name}
