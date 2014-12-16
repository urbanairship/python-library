def scheduled_time(timestamp):
    """Specify a time for the delivery of this push.

    :param timestamp: A ``datetime.datetime`` object.

    """

    return {'scheduled_time': timestamp.strftime('%Y-%m-%dT%H:%M:%S')}
