import datetime
import json
import unittest

import mock
import requests

import urbanairship as ua


class TestPush(unittest.TestCase):

    def test_full_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert='Hello')
        p.options = {}
        p.device_types = ua.all_
        p.message = ua.message("Title", "Body", "text/html", "utf8")

        self.assertEqual(p.payload, {
            "audience": "all",
            "notification": {"alert": "Hello"},
            "device_types": "all",
            "options": {},
            "message": {
                "title": "Title",
                "body": "Body",
                "content_type": "text/html",
                "content_encoding": "utf8",
            }
        })

    def test_full_scheduled_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert='Hello')
        p.options = {}
        p.device_types = ua.all_
        p.message = ua.message("Title", "Body", "text/html", "utf8")
        sched = ua.ScheduledPush(None)
        sched.push = p
        sched.name = "a schedule"
        sched.schedule = ua.scheduled_time(
            datetime.datetime(2014, 1, 1, 12, 0, 0))

        self.assertEqual(sched.payload, {
            "name": "a schedule",
            "schedule": {'scheduled_time': '2014-01-01T12:00:00'},
            "push": {
                "audience": "all",
                "notification": {"alert": "Hello"},
                "device_types": "all",
                "options": {},
                "message": {
                    "title": "Title",
                    "body": "Body",
                    "content_type": "text/html",
                    "content_encoding": "utf8",
                },
            }
        })

    def test_push_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = (
                '''{"push_ids": ["0492662a-1b52-4343-a1f9-c6b0c72931c0"]}'''.encode('utf-8'))
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.options = {}
            push.device_types = ua.all_
            pr = push.send()
            self.assertEqual(
                pr.push_ids, ['0492662a-1b52-4343-a1f9-c6b0c72931c0'])

    def test_schedule_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = (
                '''{"schedule_urls": ["https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0"]}'''.encode('utf-8'))
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

            self.assertEqual(sched.url,
                "https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0")

    def test_schedule_from_url(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                "name": "a schedule",
                "schedule": {"scheduled_time": "2013-07-15T18:40:20"},
                "push": {
                    "audience": "all",
                    "notification": {"alert": "Hello"},
                    "device_types": "all",
                    "options": {},
                    "message": {
                        "title": "Title",
                        "body": "Body",
                        "content_type": "text/html",
                        "content_encoding": "utf8",
                    },
                },
            }).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            url = "https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0"

            airship = ua.Airship('key', 'secret')
            sched = ua.ScheduledPush.from_url(airship, url)

            self.assertEqual(sched.push.device_types, 'all')

    def test_cancel(self):
        airship = ua.Airship('key', 'secret')
        sched = ua.ScheduledPush(airship)

        # Fail w/o URL
        self.assertRaises(ValueError, sched.cancel)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response.status_code = 204
            mock_request.return_value = response

            url = "https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0"

            sched.url = url

            sched.cancel()

    def test_update_schedule(self):
        airship = ua.Airship('key', 'secret')
        sched = ua.ScheduledPush(airship)
        # Fail w/o URL
        self.assertRaises(ValueError, sched.update)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            url = "https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0"

            response = requests.Response()
            response.status_code = 202
            response._content = (
                '''{"schedule_urls": ["https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0"]}'''.encode('utf-8'))

            mock_request.return_value = response

            sched.url = url
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.device_types = ua.all_
            sched.push = push
            sched.schedule = ua.scheduled_time(datetime.datetime.now())

            sched.update()
