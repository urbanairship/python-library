import datetime
import unittest

import mock
import requests

import urbanairship as ua


class TestPush(unittest.TestCase):

    def test_push_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = (
                '''{"push_ids": ["0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.device_types = ua.all_
            push.send()

    def test_schedule_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = (
                '''{"push_ids": ["0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            sched = ua.ScheduledPush(airship)
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.device_types = ua.all_
            sched.push = push
            sched.schedule = ua.scheduled_time(datetime.datetime.now())
            sched.send()
