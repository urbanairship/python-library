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
