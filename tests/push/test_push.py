import datetime
import json
import unittest

import mock
import requests
import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET
from urbanairship.enums import LiveActivityEvent, LiveUpdateEvent


class TestPush(unittest.TestCase):
    def test_full_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert="Hello")
        p.options = ua.options(expiry=10080)
        p.campaigns = ua.campaigns(categories=["kittens", "tacos", "horse_racing"])
        p.device_types = ua.all_
        p.message = ua.message(
            title="Title",
            body="Body",
            content_type="text/html",
            content_encoding="utf8",
            extra={"more": "stuff"},
            expiry=10080,
            icons={"list_icon": "http://cdn.example.com/message.png"},
            options={"some_delivery_option": "true"},
        )
        p.localizations = [
            ua.localization(
                country="us", language="es", notification=ua.notification(alert="Hola")
            )
        ]
        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "notification": {"alert": "Hello"},
                "device_types": "all",
                "options": {"expiry": 10080},
                "campaigns": {"categories": ["kittens", "tacos", "horse_racing"]},
                "message": {
                    "title": "Title",
                    "body": "Body",
                    "content_type": "text/html",
                    "content_encoding": "utf8",
                    "extra": {"more": "stuff"},
                    "expiry": 10080,
                    "icons": {"list_icon": "http://cdn.example.com/message.png"},
                    "options": {"some_delivery_option": "true"},
                },
                "localizations": [
                    {
                        "language": "es",
                        "country": "us",
                        "notification": {"alert": "Hola"},
                    }
                ],
            },
        )

    def test_web_push(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert="Hello",
            web={
                "title": "This is a title.",
                "icon": {"url": "https://example.com/icon.png"},
                "extra": {"attribute": "id"},
                "time_to_live": 12345,
                "require_interaction": False,
            },
        )
        p.device_types = "web"

        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "device_types": "web",
                "notification": {
                    "alert": "Hello",
                    "web": {
                        "title": "This is a title.",
                        "icon": {"url": "https://example.com/icon.png"},
                        "extra": {"attribute": "id"},
                        "time_to_live": 12345,
                        "require_interaction": False,
                    },
                },
            },
        )

    def test_web_push_to_channel(self):
        p = ua.Push(None)
        p.audience = ua.channel("7bdf2204-4c1b-4a23-8648-9ea74c6be4a3")
        p.notification = ua.notification(alert="Hello individual")
        p.device_types = "web"

        self.assertEqual(
            p.payload,
            {
                "audience": {"channel": "7bdf2204-4c1b-4a23-8648-9ea74c6be4a3"},
                "notification": {"alert": "Hello individual"},
                "device_types": "web",
            },
        )

    def test_open_channel_push(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert="Hello closed channels",
            open_platform={
                "email": {
                    "alert": "Hello open channels",
                    "title": "This is a title.",
                    "summary": "A longer summary of some content",
                    "media_attachment": "https://example.com/cat_standing_up.jpeg",
                    "extra": {"attribute": "id"},
                    "interactive": {
                        "type": "ua_yes_no_foreground",
                        "button_actions": {
                            "yes": {
                                "open": {
                                    "content": "https://www.urbanairship.com",
                                    "type": "url",
                                }
                            },
                            "no": {"app_defined": {"foo": "bar"}},
                        },
                    },
                }
            },
        )
        p.device_types = "open::email"
        self.assertDictEqual(
            p.payload,
            {
                "audience": "all",
                "device_types": "open::email",
                "notification": {
                    "alert": "Hello closed channels",
                    "open::email": {
                        "alert": "Hello open channels",
                        "title": "This is a title.",
                        "summary": "A longer summary of some content",
                        "media_attachment": "https://example.com/cat_standing_up.jpeg",
                        "extra": {"attribute": "id"},
                        "interactive": {
                            "type": "ua_yes_no_foreground",
                            "button_actions": {
                                "yes": {
                                    "open": {
                                        "content": "https://www.urbanairship.com",
                                        "type": "url",
                                    }
                                },
                                "no": {"app_defined": {"foo": "bar"}},
                            },
                        },
                    },
                },
            },
        )

    def test_open_channel_push_to_channel(self):
        p = ua.Push(None)
        p.audience = ua.open_channel("7bdf2204-4c1b-4a23-8648-9ea74c6be4a3")
        p.notification = ua.notification(alert="Hello individual")
        p.device_types = "open::sms"

        self.assertEqual(
            p.payload,
            {
                "audience": {"open_channel": "7bdf2204-4c1b-4a23-8648-9ea74c6be4a3"},
                "notification": {"alert": "Hello individual"},
                "device_types": "open::sms",
            },
        )

    def test_actions(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert="Hello",
            actions=ua.actions(
                add_tag="new_tag",
                remove_tag="old_tag",
                share="Check out Urban Airship!",
                open_={"type": "url", "content": "http://www.urbanairship.com"},
                app_defined={"some_app_defined_action": "some_values"},
            ),
        )
        p.device_types = ua.all_
        p.message = ua.message(
            title="Title",
            body="Body",
            content_type="text/html",
            content_encoding="utf8",
        )

        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "notification": {
                    "alert": "Hello",
                    "actions": {
                        "add_tag": "new_tag",
                        "remove_tag": "old_tag",
                        "share": "Check out Urban Airship!",
                        "open": {
                            "type": "url",
                            "content": "http://www.urbanairship.com",
                        },
                        "app_defined": {"some_app_defined_action": "some_values"},
                    },
                },
                "device_types": "all",
                "message": {
                    "title": "Title",
                    "body": "Body",
                    "content_type": "text/html",
                    "content_encoding": "utf8",
                },
            },
        )

    def test_interactive(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert="Hey, click yes!",
            interactive=ua.interactive(
                type="some_type",
                button_actions={
                    "yes": {
                        "add_tag": "clicked_yes",
                        "remove_tag": "never_clicked_yes",
                        "open": {
                            "type": "url",
                            "content": "http://www.urbanairship.com",
                        },
                    },
                    "no": {"add_tag": "hater"},
                },
            ),
        )
        p.device_types = ua.all_
        p.message = ua.message(
            title="Title",
            body="Body",
            content_type="text/html",
            content_encoding="utf8",
        )

        self.assertEqual(
            p.payload,
            {
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
                                    "content": "http://www.urbanairship.com",
                                },
                            },
                            "no": {"add_tag": "hater"},
                        },
                    },
                },
                "device_types": "all",
                "message": {
                    "title": "Title",
                    "body": "Body",
                    "content_type": "text/html",
                    "content_encoding": "utf8",
                },
            },
        )

    def test_in_app(self):
        self.maxDiff = None

        p = ua.Push(None)
        p.audience = ua.all_
        p.in_app = ua.in_app(
            alert="Alert message",
            display_type="banner",
            display={"position": "top", "duration": "500"},
            interactive=ua.interactive(
                type="ua_yes_no_foreground",
                button_actions={
                    "yes": ua.actions(
                        open_={"type": "url", "content": "https://www.urbanairship.com"}
                    )
                },
            ),
        )

        self.assertEqual(
            p.in_app,
            {
                "alert": "Alert message",
                "display_type": "banner",
                "display": {"position": "top", "duration": "500"},
                "interactive": {
                    "button_actions": {
                        "yes": {
                            "open": {
                                "content": "https://www.urbanairship.com",
                                "type": "url",
                            }
                        }
                    },
                    "type": "ua_yes_no_foreground",
                },
            },
        )

    def test_sms_push_to_sender(self):
        p = ua.Push(None)
        p.audience = ua.sms_sender("12345")
        p.notification = ua.notification(alert="sending sms to all with sender")
        p.device_types = ua.device_types("sms")

        self.assertEqual(
            p.payload,
            {
                "audience": {"sms_sender": "12345"},
                "device_types": ["sms"],
                "notification": {"alert": "sending sms to all with sender"},
            },
        )

    def test_sms_push_to_id(self):
        p = ua.Push(None)
        p.audience = ua.sms_id("01230984567", "12345")
        p.notification = ua.notification(alert="send sms to id with sender and msisdn")
        p.device_types = ua.device_types("sms")

        self.assertEqual(
            p.payload,
            {
                "audience": {"sms_id": {"sender": "12345", "msisdn": "01230984567"}},
                "device_types": ["sms"],
                "notification": {"alert": "send sms to id with sender and msisdn"},
            },
        )

    def test_sms_overrides(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert="top level alert",
            sms=ua.sms(
                alert="sms override alert",
                expiry="2018-04-01T12:00:00",
                shorten_links=True,
            ),
        )
        p.device_types = ua.device_types("sms")

        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "device_types": ["sms"],
                "notification": {
                    "alert": "top level alert",
                    "sms": {
                        "alert": "sms override alert",
                        "expiry": "2018-04-01T12:00:00",
                        "shorten_links": True,
                    },
                },
            },
        )

    def test_mms_overrides(self):
        mms_payload = ua.mms(
            fallback_text="an airbag saved my life",
            content_type="image/gif",
            url="https://c.tenor.com/ZhKMg4_yCTgAAAAC/surprised-pikachu.gif",
            shorten_links=True,
            content_length=1000,
            text="hey man slow down",
            subject="this is what you get",
        )

        self.assertEqual(
            mms_payload,
            {
                "mms": {
                    "subject": "this is what you get",
                    "fallback_text": "an airbag saved my life",
                    "shorten_links": True,
                    "slides": [
                        {
                            "text": "hey man slow down",
                            "media": {
                                "url": "https://c.tenor.com/ZhKMg4_yCTgAAAAC/surprised-pikachu.gif",
                                "content_type": "image/gif",
                                "content_length": 1000,
                            },
                        }
                    ],
                }
            },
        )

    def test_email_overrides(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            email=ua.email(
                message_type="transactional",
                plaintext_body="hello",
                reply_to="tegan@sara.xyz",
                sender_address="the@con.abc",
                sender_name="test_name",
                subject="hi",
                html_body="<html>so rich!</html>",
                attachments=["16d7442e-5ad4-4ab2-b65a-99c63e39a1d6"],
            )
        )
        p.device_types = ua.device_types("email")

        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "device_types": ["email"],
                "notification": {
                    "email": {
                        "message_type": "transactional",
                        "plaintext_body": "hello",
                        "reply_to": "tegan@sara.xyz",
                        "sender_address": "the@con.abc",
                        "sender_name": "test_name",
                        "subject": "hi",
                        "html_body": "<html>so rich!</html>",
                        "attachments": [{"id": "16d7442e-5ad4-4ab2-b65a-99c63e39a1d6"}],
                    }
                },
            },
        )

    def test_email_missing_device_type(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            email=ua.email(
                message_type="transactional",
                plaintext_body="hello",
                reply_to="tegan@sara.xyz",
                sender_address="the@con.abc",
                sender_name="test_name",
                subject="hi",
                html_body="<html>so rich!</html>",
            )
        )
        p.device_types = ua.device_types("ios")

        with self.assertRaises(ValueError):
            p.send()

    def test_email_with_device_type_all(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            email=ua.email(
                message_type="transactional",
                plaintext_body="hello",
                reply_to="tegan@sara.xyz",
                sender_address="the@con.abc",
                sender_name="test_name",
                subject="hi",
                html_body="<html>so rich!</html>",
            )
        )
        p.device_types = ua.all_

        with self.assertRaises(ValueError):
            p.send()

    def test_email_missing_override(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert="no email to be found!")
        p.device_types = ua.device_types("email")

        with self.assertRaises(ValueError):
            p.send()

    def test_standard_ios_opts(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert="Top level alert",
            ios=ua.ios(alert="iOS override alert", sound="cat.caf"),
        )
        p.device_types = ua.device_types("ios")

        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "device_types": ["ios"],
                "notification": {
                    "alert": "Top level alert",
                    "ios": {"alert": "iOS override alert", "sound": "cat.caf"},
                },
            },
        )

    def test_ios_overrides(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            ios=ua.ios(
                alert={
                    "title": "this is",
                    "body": "backwards",
                    "summary-arg": "Matmos",
                    "summary-arg-count": 1,
                },
                sound={"name": "Amplified Synapse", "volume": 0.8, "critical": False},
                thread_id="plastic minor",
                priority=10,
                badge=3,
                extra={"office": "furniture"},
                mutable_content=False,
                title="this is",
                subtitle="backwards",
                collapse_id="nugent sand",
                interruption_level="critical",
                relevance_score=0.75,
                target_content_id="big day coming",
                media_attachment=ua.media_attachment(
                    url="https://www.testurl.com",
                    content={
                        "title": "Moustache Twirl",
                        "body": "Have you ever seen a moustache like this?!",
                    },
                    options={
                        "crop": {"height": 0.5, "width": 0.5, "x": 0.25, "y": 0.25},
                        "time": 15,
                    },
                ),
                live_activity=ua.live_activity(
                    event=LiveActivityEvent.UPDATE,
                    alert={"title": "test", "sound": "test", "body": "test"},
                    name="test",
                    priority=5,
                    content_state={"test": "test"},
                    relevance_score=1.0,
                    stale_date=1234,
                    dismissal_date=1234,
                    timestamp=1234,
                ),
            )
        )
        p.options = ua.options(10080)
        p.device_types = "ios"
        p.message = ua.message(
            title="Title",
            body="Body",
            content_type="text/html",
            content_encoding="utf8",
        )

        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "notification": {
                    "ios": {
                        "alert": {
                            "title": "this is",
                            "body": "backwards",
                            "summary-arg": "Matmos",
                            "summary-arg-count": 1,
                        },
                        "badge": 3,
                        "sound": {
                            "name": "Amplified Synapse",
                            "volume": 0.8,
                            "critical": False,
                        },
                        "extra": {"office": "furniture"},
                        "title": "this is",
                        "mutable_content": False,
                        "subtitle": "backwards",
                        "media_attachment": {
                            "url": "https://www.testurl.com",
                            "content": {
                                "title": "Moustache Twirl",
                                "body": "Have you ever seen a moustache like this?!",
                            },
                            "options": {
                                "crop": {
                                    "height": 0.5,
                                    "width": 0.5,
                                    "x": 0.25,
                                    "y": 0.25,
                                },
                                "time": 15,
                            },
                        },
                        "priority": 10,
                        "collapse_id": "nugent sand",
                        "thread_id": "plastic minor",
                        "interruption_level": "critical",
                        "relevance_score": 0.75,
                        "target_content_id": "big day coming",
                        "live_activity": {
                            "alert": {"title": "test", "sound": "test", "body": "test"},
                            "event": "update",
                            "name": "test",
                            "priority": 5,
                            "content_state": {"test": "test"},
                            "relevance_score": 1.0,
                            "stale_date": 1234,
                            "dismissal_date": 1234,
                            "timestamp": 1234,
                        },
                    }
                },
                "device_types": "ios",
                "options": {"expiry": 10080},
                "message": {
                    "title": "Title",
                    "body": "Body",
                    "content_type": "text/html",
                    "content_encoding": "utf8",
                },
            },
        )

    def test_full_scheduled_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert="Hello")
        p.options = ua.options(expiry=10080)
        p.device_types = ua.all_
        p.message = ua.message(
            title="Title",
            body="Body",
            content_type="text/html",
            content_encoding="utf8",
            extra={"more": "stuff"},
            expiry=10080,
            icons={"list_icon": "http://cdn.example.com/message.png"},
            options={"some_delivery_option": "true"},
        )
        sched = ua.ScheduledPush(None)
        sched.push = p
        sched.name = "a schedule"
        sched.schedule = ua.scheduled_time(datetime.datetime(2014, 1, 1, 12, 0, 0))

        self.assertEqual(
            sched.payload,
            {
                "name": "a schedule",
                "schedule": {"scheduled_time": "2014-01-01T12:00:00"},
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
                        "extra": {"more": "stuff"},
                        "expiry": 10080,
                        "icons": {"list_icon": "http://cdn.example.com/message.png"},
                        "options": {"some_delivery_option": "true"},
                    },
                },
            },
        )

    def test_local_scheduled_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert="Hello")
        p.options = ua.options(10080)
        p.device_types = ua.all_
        p.message = ua.message(
            title="Title",
            body="Body",
            content_type="text/html",
            content_encoding="utf8",
        )

        sched = ua.ScheduledPush(None)
        sched.push = p
        sched.name = "a schedule in device local time"
        sched.schedule = ua.local_scheduled_time(
            datetime.datetime(2015, 1, 1, 12, 0, 0)
        )

        self.assertEqual(
            sched.payload,
            {
                "name": "a schedule in device local time",
                "schedule": {"local_scheduled_time": "2015-01-01T12:00:00"},
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
            },
        )

    def test_push_success(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {"push_ids": ["0492662a-1b52-4343-a1f9-c6b0c72931c0"]}
            ).encode("utf-8")
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert="Hello")
            push.options = ua.options(expiry=10080)
            push.device_types = ua.all_
            pr = push.send()
            self.assertEqual(pr.push_ids, ["0492662a-1b52-4343-a1f9-c6b0c72931c0"])

    def test_schedule_success(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "schedule_urls": [
                        (
                            "https://go.urbanairship.com/api/schedules/"
                            "0492662a-1b52-4343-a1f9-c6b0c72931c0"
                        )
                    ]
                }
            ).encode("utf-8")
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sched = ua.ScheduledPush(airship)
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert="Hello")
            push.device_types = ua.all_
            sched.push = push
            sched.schedule = ua.scheduled_time(datetime.datetime.now())
            sched.send()

            self.assertEquals(
                sched.url,
                (
                    "https://go.urbanairship.com/api/schedules/"
                    "0492662a-1b52-4343-a1f9-c6b0c72931c0"
                ),
            )

    def test_scheduled_template(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "schedule_urls": [
                        "https://go.urbanairship.com/api/schedules/40fe5b31-8997-4819-9aeb-e6c4ae95e5d3"
                    ]
                }
            ).encode("utf-8")
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sched = ua.ScheduledPush(airship)
            sched.schedule = ua.scheduled_time(datetime.datetime.now())

            template_push = airship.create_template_push()
            template_push.audience = ua.ios_channel(
                "780ba0c5-45be-4f29-befa-39135cb05b59"
            )
            template_push.device_types = ua.device_types("ios")
            template_push.merge_data = ua.merge_data(
                template_id="780ba0c5-45be-4f29-befa-39135cb05b59",
                substitutions={"key": "value"},
            )

            sched.push = template_push
            sched.send()

            self.assertEqual(
                sched.url,
                "https://go.urbanairship.com/api/schedules/40fe5b31-8997-4819-9aeb-e6c4ae95e5d3",
            )

    def test_local_schedule_success(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "schedule_urls": [
                        (
                            "https://go.urbanairship.com/api/schedules/"
                            "0492662a-1b52-4343-a1f9-c6b0c72931c0"
                        )
                    ]
                }
            ).encode("utf-8")
            response.status_code = 202
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sched = ua.ScheduledPush(airship)
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert="Hello")
            push.device_types = ua.all_
            sched.push = push
            sched.schedule = ua.local_scheduled_time(datetime.datetime.now())
            sched.send()

            self.assertEquals(
                sched.url,
                (
                    "https://go.urbanairship.com/api/schedules/"
                    "0492662a-1b52-4343-a1f9-c6b0c72931c0"
                ),
            )

    def test_schedule_from_url(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
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
                }
            ).encode("utf-8")

            response.status_code = 200
            mock_request.return_value = response

            url = (
                "https://go.urbanairship.com/api/schedules/"
                "0492662a-1b52-4343-a1f9-c6b0c72931c0"
            )

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            sched = ua.ScheduledPush.from_url(airship, url)

            self.assertEqual(sched.push.device_types, "all")

    def test_cancel(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        sched = ua.ScheduledPush(airship)

        # Fail w/o URL
        self.assertRaises(ValueError, sched.cancel)

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response.status_code = 204
            mock_request.return_value = response

            url = (
                "https://go.urbanairship.com/api/schedules/"
                "0492662a-1b52-4343-a1f9-c6b0c72931c0"
            )
            sched.url = url

            sched.cancel()

    def test_update_schedule(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        sched = ua.ScheduledPush(airship)
        # Fail w/o URL
        self.assertRaises(ValueError, sched.update)

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            url = (
                "https://go.urbanairship.com/api/schedules/"
                "0492662a-1b52-4343-a1f9-c6b0c72931c0"
            )

            response = requests.Response()
            response.status_code = 202
            response._content = json.dumps(
                {
                    "schedule_urls": [
                        (
                            "https://go.urbanairship.com/api/schedules/"
                            "0492662a-1b52-4343-a1f9-c6b0c72931c0"
                        )
                    ]
                }
            ).encode("utf-8")

            mock_request.return_value = response

            sched.url = url
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert="Hello")
            push.device_types = ua.all_
            sched.push = push
            sched.schedule = ua.scheduled_time(datetime.datetime.now())

            sched.update()

    def test_schedules_listing(self):
        self.url1 = "https://go.urbanairship.com/api/schedules/16153636-4434-441f-bad4-86ab0f1778bc"
        self.url2 = "https://go.urbanairship.com/api/schedules/ee03b71b-5b88-4b87-93cf-2d9dc8b87e7c"

        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "ok": True,
                    "count": 2,
                    "schedules": [
                        {
                            "url": "https://go.urbanairship.com/api/schedules/16153636-4434-441f-bad4-86ab0f1778bc",
                            "schedule": {"scheduled_time": "2018-10-09T18:43:34"},
                            "name": "Test1 Schedule",
                            "push": {
                                "audience": "all",
                                "device_types": "all",
                                "notification": {"alert": "Hello, python!"},
                            },
                            "push_ids": ["a4ed2e7b-de88-4fbc-9ccc-eb9de75b7c6e"],
                        },
                        {
                            "url": "https://go.urbanairship.com/api/schedules/ee03b71b-5b88-4b87-93cf-2d9dc8b87e7c",
                            "schedule": {"local_scheduled_time": "2018-12-29T20:41:29"},
                            "push": {
                                "audience": {"named_user": "python_library"},
                                "device_types": ["ios", "android", "amazon"],
                                "notification": {"alert": "Hello Python Local Time"},
                            },
                            "push_ids": [
                                "b13b40f3-7a2e-40c5-8df1-cb657878e983",
                                "dc9213b3-19f0-49b4-91b3-080e26f96293",
                                "3c13423d-5f2d-4fdc-8a34-c64bcd09d564",
                                "9bd0f266-6e52-474d-92ca-4688a17ebba1",
                                "d264dc5e-025d-4ed1-9cc9-ee694f1decf5",
                                "f4888ef7-672f-414e-a3a1-2b0d085f0e87",
                                "d7c977ec-be29-4b1f-89b0-13f734b9524a",
                                "82e4966a-8b45-4500-92bb-9c329f284f29",
                                "dd636364-4347-4fcc-bd8c-d5c3a60e94a0",
                                "7bc81dac-98df-4c24-994c-4129c02d8ed2",
                                "55da24c0-2a85-46d4-a8a8-689e1a1a05c1",
                                "068a89c9-aa92-47bd-ac11-ce581b69e328",
                                "ba91a074-28c5-4eaa-b45b-a76638e9425c",
                                "2d1bfe48-f7b6-4c6c-a2c7-37e0b2d300cc",
                                "410c76b8-e732-465d-bc53-04c89f82921a",
                                "e319d847-a6da-4c9c-9179-1c3d73129cf2",
                                "e4209428-9e50-4c86-a105-4dbb52b9060a",
                                "c9fbd026-7c51-4835-9acb-1fc5a45286d4",
                                "c8b914a7-6a29-4faa-a817-cf4ed2874ab8",
                                "881ad454-ff25-481e-8f58-06f02082c856",
                                "1b317ccd-25a6-481c-a200-e6cf67cf079f",
                                "fec10a5a-1b8c-4e2e-bff5-26dd5edf3bce",
                                "2a3ee2c0-490b-4f9b-92c0-bebaf45eba0a",
                                "832dbaac-135f-490d-bd07-50e787c29d18",
                                "f5bb80ab-6503-4d37-be93-eeff4f25db01",
                                "a995e469-87cb-41a3-b919-42dda38344e9",
                                "cda3e7a0-7e3a-40cf-b4bd-56e0c0f5784c",
                                "b4c7272f-f14a-4f08-8f62-e69b567c83fb",
                                "5899bb33-7a78-4793-9cbb-ca3714192ba2",
                                "c6bbfb10-95a4-4cfa-a73c-ece3b48d429c",
                                "582a224e-3f3f-4188-beab-17e963ecefbc",
                                "d5cf17e9-dfd9-40f3-8934-71f53535fb7c",
                                "86e9ec5c-207e-4a66-ab0b-cfeb4b141014",
                                "f6673b76-d2f0-472e-ac54-01554d5d97b4",
                                "e0c872c2-6adb-45d3-8f6d-2c3ba0a32257",
                                "0df19a37-4297-465f-867c-d436889f5085",
                                "f3d94825-331c-4562-b706-18d65fa914ab",
                                "eed2ce1e-e221-4d0c-bfd1-f9dd253e20e4",
                                "5e25be82-a68c-47a6-852b-911108214209",
                                "4a91e9d9-10f6-4264-bc0c-a1096722d95f",
                                "3c453695-7051-42e9-ab57-4912151c7e42",
                                "2f390cf6-fcb1-4492-b47f-fb7b58c717a6",
                            ],
                        },
                    ],
                }
            ).encode("utf-8")

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)

            schedule_listing = []

            for schedule in ua.ScheduledList(airship):
                schedule_listing.append(schedule)

            self.assertEquals(schedule_listing[0].url, self.url1)
            self.assertEquals(schedule_listing[1].url, self.url2)

            self.assertEquals(len(schedule_listing[0].push_ids), 1)
            self.assertEquals(len(schedule_listing[1].push_ids), 42)

    def test_options_int_expiry(self):
        opt = ua.options(expiry=10080)
        self.assertEqual(opt, {"expiry": 10080})

    def test_options_date_expiry(self):
        opt = ua.options(expiry="2015-04-01T12:00:00")
        self.assertEqual(opt, {"expiry": "2015-04-01T12:00:00"})

    def test_campaigns_list(self):
        cam = ua.campaigns(categories=["bugs", "worms"])
        self.assertEqual(cam, {"categories": ["bugs", "worms"]})

        with self.assertRaises(ValueError):
            ua.campaigns(categories=[])

        with self.assertRaises(TypeError):
            ua.campaigns({"categories": ["bugs", "worms"]})

    def test_campaigns_str(self):
        cam = ua.campaigns(categories="bugs")
        self.assertEqual(cam, {"categories": ["bugs"]})

        with self.assertRaises(ValueError):
            ua.campaigns(
                categories="""a_long_string_so_long_its_longer_than_
                                    sixty_four_characters_too_long"""
            )

    def test_amazon_overrides(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            amazon=ua.amazon(
                alert="overridden alert",
                consolidation_key="consolidated on",
                expires_after=123456789,
                extra={"key": "value"},
                title="this is the title",
                summary="summarized",
                notification_tag="you are it",
                notification_channel="my cool channel",
                icon="icon.img",
                icon_color="#1234ff",
            )
        )
        p.device_types = ua.device_types("amazon")

        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "device_types": ["amazon"],
                "notification": {
                    "amazon": {
                        "alert": "overridden alert",
                        "consolidation_key": "consolidated on",
                        "expires_after": 123456789,
                        "extra": {"key": "value"},
                        "title": "this is the title",
                        "summary": "summarized",
                        "notification_tag": "you are it",
                        "notification_channel": "my cool channel",
                        "icon": "icon.img",
                        "icon_color": "#1234ff",
                    }
                },
            },
        )

    def test_standard_amazon_push(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert="top level alert", amazon=ua.amazon(alert="amazon override alert")
        )
        p.device_types = ua.device_types("amazon")

        self.assertEqual(
            p.payload,
            {
                "audience": "all",
                "device_types": ["amazon"],
                "notification": {
                    "alert": "top level alert",
                    "amazon": {"alert": "amazon override alert"},
                },
            },
        )

    def test_localization(self):
        localization = ua.localization(
            country="fr",
            language="fr",
            notification=ua.notification(alert="bonjour"),
            in_app=ua.in_app(alert="bonjour", display_type="banner"),
            message=ua.message(title="bonjour", body="<html><h1>Bonjour!</h1></html>"),
        )
        self.assertEqual(
            localization,
            {
                "country": "fr",
                "language": "fr",
                "notification": {"alert": "bonjour"},
                "in_app": {"alert": "bonjour", "display_type": "banner"},
                "message": {
                    "title": "bonjour",
                    "body": "<html><h1>Bonjour!</h1></html>",
                },
            },
        )

    def test_localization_raises_no_country_lang(self):
        with self.assertRaises(ValueError):
            ua.localization(notification=ua.notification(alert="oops"))

    def testlocalization_raises_no_content(self):
        with self.assertRaises(ValueError):
            ua.localization(country="us", language="en")

    def test_options_expiry_as_int():
        result = ua.options(expiry=300)
        assert result == {"expiry": 300}

    def test_options_expiry_as_string():
        result = ua.options(expiry="2023-10-19T10:00:00Z")
        assert result == {"expiry": "2023-10-19T10:00:00Z"}

    def test_options_with_multiple_values():
        result = ua.options(
            expiry="2023-10-19T10:00:00Z",
            bypass_frequency_limits=True,
            bypass_holdout_groups=True,
            no_throttle=True,
            omit_from_activity_log=True,
            personalization=True,
            redact_payload=True,
        )
        expected_result = {
            "expiry": "2023-10-19T10:00:00Z",
            "bypass_frequency_limits": True,
            "bypass_holdout_groups": True,
            "no_throttle": True,
            "omit_from_activity_log": True,
            "personalization": True,
            "redact_payload": True,
        }
        assert result == expected_result

    def test_valid_live_activity(self):
        result = ua.live_activity(
            event=LiveActivityEvent.UPDATE,
            name="TestActivity",
            alert={"body": "Test body", "sound": "default", "title": "Test Title"},
            priority=10,
        )
        self.assertIn("alert", result)
        self.assertEqual(result["event"], "update")
        self.assertEqual(result["name"], "TestActivity")
        self.assertEqual(result["priority"], 10)

    def test_invalid_alert(self):
        with self.assertRaises(ValueError):
            ua.live_activity(
                event=LiveActivityEvent.UPDATE,
                name="TestActivity",
                alert={"other_key": "test", "title": "test"},
                priority=10,
            )

    def test_missing_name_live_activity(self):
        with self.assertRaises(ValueError):
            ua.live_activity(event=LiveActivityEvent.END, priority=10)

    def test_valid_live_update(self):
        result = ua.live_update(
            event=LiveUpdateEvent.START,
            name="TestUpdate",
            content_state={"key": "value"},
        )
        self.assertEqual(result["event"], "start")
        self.assertEqual(result["name"], "TestUpdate")
        self.assertIn("content_state", result)

    def test_invalid_content_state(self):
        with self.assertRaises(TypeError):
            ua.live_update(
                event=LiveUpdateEvent.UPDATE, name="TestUpdate", content_state="invalid"
            )

    def test_missing_name_live_update(self):
        with self.assertRaises(ValueError):
            ua.live_update(event=LiveUpdateEvent.END)
