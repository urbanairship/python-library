from urbanairship import common
from urbanairship.push import ScheduledPush


class ScheduledList(common.IteratorParent):
    """
    Iterator for listing all scheduled messages.

    :ivar limit: Number of entries to fetch in a paginated request.
    :returns Each ``next`` returns a :py:class:`ScheduledPush` object.
    """
    next_url = common.SCHEDULES_URL
    data_attribute = 'schedules'
    id_key = 'url'
    instance_class = ScheduledPush

    def __init__(self, airship, limit=None):
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
