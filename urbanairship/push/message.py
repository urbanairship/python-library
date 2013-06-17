import re

# Valid autobadge values: auto, +N, -N
VALID_AUTOBADGE = re.compile(r'^(auto|[+-][\d]+)$')


def notification(alert=None, ios=None, android=None, blackberry=None, wns=None,
        mpns=None):
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if ios is not None:
        payload['ios'] = ios
    if android is not None:
        payload['android'] = android
    if blackberry is not None:
        payload['blackberry'] = blackberry
    if wns is not None:
        payload['wns'] = wns
    if mpns is not None:
        payload['mpns'] = mpns
    if not payload:
        raise ValueError("Notification body may not be empty")
    return payload


def ios(alert=None, badge=None, sound=None, content_available=None,
        extra=None):
    """iOS/APNS specific payload"""

    payload = {}
    if alert is not None:
        if not isinstance(alert, basestring) or isinstance(alert, dict):
            raise ValueError("iOS alert must be a string or dictionary")
        payload['alert'] = alert
    if badge is not None:
        if not isinstance(badge, basestring) or isinstance(alert, int):
            raise ValueError("iOS badge must be an integer or string")
        if not VALID_AUTOBADGE.match(badge):
            raise ValueError("Invalid iOS autobadge value")
        payload['badge'] = badge
    if sound is not None:
        payload['sound'] = sound
    if content_available:
        payload['content-available'] = 1
    if extra is not None:
        payload['extra'] = extra
    return payload


def android(alert=None, collapse_key=None, time_to_live=None,
        delay_while_idle=False, extra=None):
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if collapse_key is not None:
        payload['collapse_key'] = collapse_key
    if time_to_live is not None:
        payload['time_to_live'] = time_to_live
    if delay_while_idle:
        payload['delay_while_idle'] = True
    if extra is not None:
        payload['extra'] = extra
    return payload


def blackberry(alert=None, body=None, content_type=None):
    payload = {}
    if alert is not None:
        payload['body'] = alert
        payload['content_type'] = 'text/plain'
    elif body is not None and content_type is not None:
        payload['body'] = body
        payload['content_type'] = content_type
    else:
        raise ValueError("BlackBerry body and content_type may not be empty")
    return payload


def wns_payload(alert=None, toast=None, tile=None, badge=None):
    if len(filter(None, (alert, toast, tile, badge))) != 1:
        raise ValueError("WNS payload must have one notification type.")
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if toast is not None:
        payload['toast'] = toast
    if tile is not None:
        payload['tile'] = tile
    if badge is not None:
        payload['badge'] = badge
    return payload


def mpns_payload(alert=None, toast=None, tile=None):
    if len(filter(None, (alert, toast, tile))) != 1:
        raise ValueError("MPNS payload must have one notification type.")
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if toast is not None:
        payload['toast'] = toast
    if tile is not None:
        payload['tile'] = tile
    return payload


def device_types(*types):
    for t in types:
        if t not in ('ios', 'android' 'blackberry' 'wns' 'mpns' 'adm'):
            raise ValueError("Invalid device type %s" % t)
    return [t for t in types]
