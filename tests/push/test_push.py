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
        p.options = ua.options(expiry=10080)
        p.device_types = ua.all_
        p.message = ua.message(title="Title", body="Body",
                               content_type="text/html",
                               content_encoding="utf8",
                               extra={"more": "stuff"},
                               expiry=10080,
                               icons={"list_icon": "http://cdn.example.com/message.png"},
                               options={"some_delivery_option": "true"}, )

        self.assertEqual(p.payload, {
            "audience": "all",
            "notification": {"alert": "Hello"},
            "device_types": "all",
            "options": {
                "expiry": 10080
            },
            "message": {
                "title": "Title",
                "body": "Body",
                "content_type": "text/html",
                "content_encoding": "utf8",
                "extra": {"more": "stuff"},
                "expiry": 10080,
                "icons": {"list_icon": "http://cdn.example.com/message.png"},
                "options": {"some_delivery_option": "true"},
            }
        })

    def test_actions(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert='Hello',
            actions=ua.actions(
                add_tag="new_tag",
                remove_tag="old_tag",
                share="Check out Urban Airship!",
                open_={
                    "type": "url",
                    "content": "http://www.urbanairship.com"
                },
                app_defined={"some_app_defined_action": "some_values"}
            )
        )
        p.device_types = ua.all_
        p.message = ua.message(title="Title", body="Body",
                               content_type="text/html",
                               content_encoding="utf8",
                               extra={"more": "stuff"},
                               expiry=10080,
                               icons={"list_icon": "http://cdn.example.com/message.png"},
                               options={"some_delivery_option": "true"}, )

        self.assertEqual(p.payload, {
            "audience": "all",
            "notification": {
                "alert": "Hello",
                "actions": {
                    "add_tag": "new_tag",
                    "remove_tag": "old_tag",
                    "share": "Check out Urban Airship!",
                    "open": {
                        "type": "url",
                        "content": "http://www.urbanairship.com"
                    },
                    "app_defined": {"some_app_defined_action": "some_values"}
                }
            },
            "device_types": "all",
            "message": {
                "title": "Title",
                "body": "Body",
                "content_type": "text/html",
                "content_encoding": "utf8",
                "extra": {"more": "stuff"},
                "expiry": 10080,
                "icons": {"list_icon": "http://cdn.example.com/message.png"},
                "options": {"some_delivery_option": "true"},
            }
        })

    def test_interactive(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert='Hey, click yes!',
            interactive=ua.interactive(
                type="some_type",
                button_actions={
                    "yes": {
                        "add_tag": "clicked_yes",
                        "remove_tag": "never_clicked_yes",
                        "open": {
                            "type": "url",
                            "content": "http://www.urbanairship.com"
                        }
                    },
                    "no": {
                        "add_tag": "hater"
                    }
                }
            )
        )
        p.device_types = ua.all_
        p.message = ua.message(title="Title", body="Body",
                               content_type="text/html",
                               content_encoding="utf8", )

        self.assertEqual(p.payload, {
            "audience": "all",
            "notification": {
                "alert": "Hey, click yes!",
                "interactive": {
                    "type": "some_type",
                    "button_actions": {
                        "yes": {
                            "add_tag": "clicked_yes",
                            "remove_tag": "never_clicked_yes",
                            "open": {
                                "type": "url",
                                "content": "http://www.urbanairship.com"
                            }
                        },
                        "no": {
                            "add_tag": "hater"
                        }
                    }
                }
            },
            "device_types": "all",
            "message": {
                "title": "Title",
                "body": "Body",
                "content_type": "text/html",
                "content_encoding": "utf8",
            }
        })

    def test_ios_alert_dict(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(ios=ua.ios(
            alert={'foo': 'bar'}
        ))
        p.options = ua.options(10080)
        p.device_types = 'ios'
        p.message = ua.message(title="Title", body="Body",
                               content_type="text/html",
                               content_encoding="utf8",
                               extra={"more": "stuff"},
                               expiry=10080,
                               icons={"list_icon": "http://cdn.example.com/message.png"},
                               options={"some_delivery_option": "true"}, )

        self.assertEqual(p.payload, {
            "audience": "all",
            "notification": {"ios": {"alert": {'foo': 'bar'}}},
            "device_types": "ios",
            "options": {
                "expiry": 10080
            },
            "message": {
                "title": "Title",
                "body": "Body",
                "content_type": "text/html",
                "content_encoding": "utf8",
                "extra": {"more": "stuff"},
                "expiry": 10080,
                "icons": {"list_icon": "http://cdn.example.com/message.png"},
                "options": {"some_delivery_option": "true"},
            }
        })

    def test_full_scheduled_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert='Hello')
        p.options = ua.options(10080)
        p.device_types = ua.all_
        p.message = ua.message(title="Title", body="Body",
                               content_type="text/html",
                               content_encoding="utf8",
                               extra={"more": "stuff"},
                               expiry=10080,
                               icons={"list_icon": "http://cdn.example.com/message.png"},
                               options={"some_delivery_option": "true"}, )
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
                "options": {
                    "expiry": 10080
                },
                "message": {
                    "title": "Title",
                    "body": "Body",
                    "content_type": "text/html",
                    "content_encoding": "utf8",
                    "extra": {"more": "stuff"},
                    "expiry": 10080,
                    "icons": {
                    "list_icon": "http://cdn.example.com/message.png"},
                    "options": {"some_delivery_option": "true"},
                },
            }
        })

    def test_local_scheduled_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert='Hello')
        p.options = ua.options(10080)
        p.device_types = ua.all_
        p.message = ua.message(title="Title", body="Body",
                               content_type="text/html",
                               content_encoding="utf8",
                               extra={"more": "stuff"},
                               expiry=10080,
                               icons={"list_icon": "http://cdn.example.com/message.png"},
                               options={"some_delivery_option": "true"}, )

        sched = ua.ScheduledPush(None)
        sched.push = p
        sched.name = "a schedule in device local time"
        sched.schedule = ua.local_scheduled_time(
            datetime.datetime(2015, 1, 1, 12, 0, 0))

        self.assertEqual(sched.payload, {
            "name": "a schedule in device local time",
            "schedule": {'local_scheduled_time': '2015-01-01T12:00:00'},
            "push": {
                "audience": "all",
                "notification": {"alert": "Hello"},
                "device_types": "all",
                "options": {
                    "expiry": 10080
                },
                "message": {
                    "title": "Title",
                    "body": "Body",
                    "content_type": "text/html",
                    "content_encoding": "utf8",
                    "extra": {"more": "stuff"},
                    "expiry": 10080,
                    "icons": {
                    "list_icon": "http://cdn.example.com/message.png"},
                    "options": {"some_delivery_option": "true"},
                },
            }
        })

    def test_push_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = (
                b'''{"push_ids": ["0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.options = ua.options(expiry=10080)
            push.device_types = ua.all_
            pr = push.send()
            self.assertEqual(
                pr.push_ids, ['0492662a-1b52-4343-a1f9-c6b0c72931c0'])

    def test_schedule_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = (
                b'''{"schedule_urls": ["https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')
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

            self.assertEquals(sched.url,
                              "https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0")

    def test_local_schedule_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = (
                b'''{"schedule_urls": ["https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship('key', 'secret')
            sched = ua.ScheduledPush(airship)
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.device_types = ua.all_
            sched.push = push
            sched.schedule = ua.local_scheduled_time(datetime.datetime.now())
            sched.send()

            self.assertEquals(sched.url,
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
                    "options": {"expiry": 10080},
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
                b'''{"schedule_urls": ["https://go.urbanairship.com/api/schedules/0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')

            mock_request.return_value = response

            sched.url = url
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.device_types = ua.all_
            sched.push = push
            sched.schedule = ua.scheduled_time(datetime.datetime.now())

            sched.update()

    def options(self):
        airship = ua.Airship('key', 'secret')
        push = ua.Push(None)
        push.audience = ua.all_
        push.notification = ua.notification(alert="Hello Expiry")
        push.options = ua.options(expiry=10080)
        push.device_types = ua.all_ 
