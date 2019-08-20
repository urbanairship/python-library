from urbanairship import common
from urbanairship.push import ScheduledPush


class ScheduledList(common.IteratorParent):
    """
    Iterator for listing all scheduled messages.

    :ivar limit: Number of entries to fetch in a paginated request.
    :returns Each ``next`` returns a :py:class:`ScheduledPush` object.
    """
    next_url = None
    data_attribute = 'schedules'
    id_key = 'url'
    instance_class = ScheduledPush

    def __init__(self, airship, limit=None):
        self.next_url = airship.urls.get('schedules_url')
        params = {'limit': limit} if limit else {}
        super(ScheduledList, self).__init__(airship, params)


def scheduled_time(timestamp):
    """Specify a time for the delivery of this push.

    :param timestamp: A ``datetime.datetime`` object.

    """

    return {'scheduled_time': timestamp.strftime('%Y-%m-%dT%H:%M:%S')}


def local_scheduled_time(timestamp):
    """Specify a time for the delivery of this push in device local time.

    :param timestamp: A ``datetime.datetime`` object.

    """

    return {'local_scheduled_time': timestamp.strftime('%Y-%m-%dT%H:%M:%S')}


def best_time(timestamp):
    """Specify a date to send the push at the best time per-device.
    Only YYYY_MM_DD are needed. Hour/minute/second information is discarded.

    :param timestamp: A ``datetime.datetime object.
    """

    return {'best_time': {'send_date': timestamp.strftime('%Y-%m-%d')}}
