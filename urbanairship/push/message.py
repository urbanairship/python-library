import re

# Valid autobadge values: auto, +N, -N
VALID_AUTOBADGE = re.compile(r'^(auto|[+-][\d]+)$')


def notification(alert=None, ios=None, android=None):
    payload = {}
    if alert is not None:
        payload['alert'] = alert
    if ios is not None:
        payload['ios'] = ios
    if android is not None:
        payload['android'] = android
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


def device_types(*types):
    for t in types:
        if t not in ('ios', 'android' 'blackberry' 'wns' 'mpns' 'adm'):
            raise ValueError("Invalid device type %s" % t)
    return [t for t in types]
