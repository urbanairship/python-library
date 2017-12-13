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
        p.campaigns = ua.campaigns(
            categories=['kittens', 'tacos', 'horse_racing']
            )
        p.device_types = ua.all_
        p.message = ua.message(
            title='Title',
            body='Body',
            content_type='text/html',
            content_encoding='utf8',
            extra={'more': 'stuff'},
            expiry=10080,
            icons={'list_icon': 'http://cdn.example.com/message.png'},
            options={'some_delivery_option': 'true'},
        )
        self.assertEqual(
            p.payload,
            {
                'audience': 'all',
                'notification': {'alert': 'Hello'},
                'device_types': 'all',
                'options': {
                    'expiry': 10080
                },
                'campaigns': {
                    'categories': ['kittens', 'tacos', 'horse_racing']
                },
                'message': {
                    'title': 'Title',
                    'body': 'Body',
                    'content_type': 'text/html',
                    'content_encoding': 'utf8',
                    'extra': {'more': 'stuff'},
                    'expiry': 10080,
                    'icons': {
                        'list_icon': 'http://cdn.example.com/message.png'
                    },
                    'options': {'some_delivery_option': 'true'},
                }
            }
        )

    def test_web_push(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert='Hello',
            web={
                'title': 'This is a title.',
                'icon': {'url': 'https://example.com/icon.png'},
                'extra': {'attribute': 'id'},
                'time_to_live': 12345,
                'require_interaction': False
            }
        )
        p.device_types = 'web'

        self.assertEqual(
            p.payload,
            {
                'audience': 'all',
                'device_types': 'web',
                'notification': {
                    'alert': 'Hello',
                    'web': {
                        'title': 'This is a title.',
                        'icon': {'url': 'https://example.com/icon.png'},
                        'extra': {'attribute': 'id'},
                        'time_to_live': 12345,
                        'require_interaction': False
                    },
                }
            }
        )

    def test_web_push_to_channel(self):
        p = ua.Push(None)
        p.audience = ua.channel('7bdf2204-4c1b-4a23-8648-9ea74c6be4a3')
        p.notification = ua.notification(
            alert='Hello individual'
        )
        p.device_types = 'web'

        self.assertEqual(
            p.payload,
            {
                'audience': {
                    'channel': '7bdf2204-4c1b-4a23-8648-9ea74c6be4a3'
                },
                'notification': {'alert': 'Hello individual'},
                'device_types': 'web'
            }
        )

    def test_open_channel_push(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert='Hello closed channels',
            open_platform={
                'email': {
                    'alert': 'Hello open channels',
                    'title': 'This is a title.',
                    'summary': 'A longer summary of some content',
                    'media_attachment':
                        'https://example.com/cat_standing_up.jpeg',
                    'extra': {'attribute': 'id'},
                    'interactive': {
                        'type': 'ua_yes_no_foreground',
                        'button_actions': {
                            'yes': {
                                'open': {
                                    'content': 'https://www.urbanairship.com',
                                    'type': 'url'
                                }
                            },
                            'no': {
                                'app_defined': {
                                    'foo': 'bar'
                                }
                            }
                        }
                    }
                }
            }
        )
        p.device_types = 'open::email'
        self.assertDictEqual(
            p.payload,
            {
                'audience': 'all',
                'device_types': 'open::email',
                'notification': {
                    'alert': 'Hello closed channels',
                    'open::email': {
                        'alert': 'Hello open channels',
                        'title': 'This is a title.',
                        'summary': 'A longer summary of some content',
                        'media_attachment':
                            'https://example.com/cat_standing_up.jpeg',
                        'extra': {'attribute': 'id'},
                        'interactive': {
                            'type': 'ua_yes_no_foreground',
                            'button_actions': {
                                'yes': {
                                    'open': {
                                        'content':
                                            'https://www.urbanairship.com',
                                        'type': 'url'
                                    }
                                },
                                'no': {
                                    'app_defined': {
                                        'foo': 'bar'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )

    def test_open_channel_push_to_channel(self):
        p = ua.Push(None)
        p.audience = ua.open_channel('7bdf2204-4c1b-4a23-8648-9ea74c6be4a3')
        p.notification = ua.notification(
            alert='Hello individual'
        )
        p.device_types = 'open::sms'

        self.assertEqual(
            p.payload,
            {
                'audience': {
                    'open_channel': '7bdf2204-4c1b-4a23-8648-9ea74c6be4a3'
                },
                'notification': {'alert': 'Hello individual'},
                'device_types': 'open::sms'
            }
        )

    def test_actions(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert='Hello',
            actions=ua.actions(
                add_tag='new_tag',
                remove_tag='old_tag',
                share='Check out Urban Airship!',
                open_={
                    'type': 'url',
                    'content': 'http://www.urbanairship.com'
                },
                app_defined={'some_app_defined_action': 'some_values'}
            )
        )
        p.device_types = ua.all_
        p.message = ua.message(
            title='Title',
            body='Body',
            content_type='text/html',
            content_encoding='utf8',
        )

        self.assertEqual(
            p.payload,
            {
                'audience': 'all',
                'notification': {
                    'alert': 'Hello',
                    'actions': {
                        'add_tag': 'new_tag',
                        'remove_tag': 'old_tag',
                        'share': 'Check out Urban Airship!',
                        'open': {
                            'type': 'url',
                            'content': 'http://www.urbanairship.com'
                        },
                        'app_defined': {
                            'some_app_defined_action': 'some_values'
                        }
                    }
                },
                'device_types': 'all',
                'message': {
                    'title': 'Title',
                    'body': 'Body',
                    'content_type': 'text/html',
                    'content_encoding': 'utf8',
                }
            }
        )

    def test_interactive(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            alert='Hey, click yes!',
            interactive=ua.interactive(
                type='some_type',
                button_actions={
                    'yes': {
                        'add_tag': 'clicked_yes',
                        'remove_tag': 'never_clicked_yes',
                        'open': {
                            'type': 'url',
                            'content': 'http://www.urbanairship.com'
                        }
                    },
                    'no': {
                        'add_tag': 'hater'
                    }
                }
            )
        )
        p.device_types = ua.all_
        p.message = ua.message(
            title='Title',
            body='Body',
            content_type='text/html',
            content_encoding='utf8',
        )

        self.assertEqual(
            p.payload,
            {
                'audience': 'all',
                'notification': {
                    'alert': 'Hey, click yes!',
                    'interactive': {
                        'type': 'some_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes',
                                'remove_tag': 'never_clicked_yes',
                                'open': {
                                    'type': 'url',
                                    'content': 'http://www.urbanairship.com'
                                }
                            },
                            'no': {
                                'add_tag': 'hater'
                            }
                        }
                    }
                },
                'device_types': 'all',
                'message': {
                    'title': 'Title',
                    'body': 'Body',
                    'content_type': 'text/html',
                    'content_encoding': 'utf8',
                }
            }
        )

    def test_in_app(self):
        self.maxDiff = None

        p = ua.Push(None)
        p.audience = ua.all_
        p.in_app = ua.in_app(
            alert='Alert message',
            display_type='banner',
            display={
                'position': 'top',
                'duration': '500'
            },
            interactive=ua.interactive(
                type='ua_yes_no_foreground',
                button_actions={
                    'yes': ua.actions(open_={
                        'type': 'url',
                        'content': 'https://www.urbanairship.com'
                    })
                }
            )
        )

        self.assertEqual(
            p.in_app,
            {
                'alert': 'Alert message',
                'display_type': 'banner',
                'display': {
                    'position': 'top',
                    'duration': '500'
                },
                'interactive': {
                    'button_actions': {
                        'yes': {
                            'open': {
                                'content': 'https://www.urbanairship.com',
                                'type': 'url'
                            }
                        }
                    },
                    'type': 'ua_yes_no_foreground'
                }
            }
        )

    def test_ios_alert_dict(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(
            ios=ua.ios(
                alert={'foo': 'bar'}
            )
        )
        p.options = ua.options(10080)
        p.device_types = 'ios'
        p.message = ua.message(
            title='Title',
            body='Body',
            content_type='text/html',
            content_encoding='utf8',
        )

        self.assertEqual(
            p.payload,
            {
                'audience': 'all',
                'notification': {
                    'ios': {
                        'alert': {
                            'foo': 'bar'
                        }
                    }
                },
                'device_types': 'ios',
                'options': {
                    'expiry': 10080
                },
                'message': {
                    'title': 'Title',
                    'body': 'Body',
                    'content_type': 'text/html',
                    'content_encoding': 'utf8',
                }
            }
        )

    def test_full_scheduled_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert='Hello')
        p.options = ua.options(10080)
        p.device_types = ua.all_
        p.message = ua.message(
            title='Title',
            body='Body',
            content_type='text/html',
            content_encoding='utf8',
            extra={'more': 'stuff'},
            expiry=10080,
            icons={
                'list_icon': 'http://cdn.example.com/message.png'
            },
            options={'some_delivery_option': 'true'},
        )
        sched = ua.ScheduledPush(None)
        sched.push = p
        sched.name = 'a schedule'
        sched.schedule = ua.scheduled_time(
            datetime.datetime(2014, 1, 1, 12, 0, 0)
        )

        self.assertEqual(
            sched.payload,
            {
                'name': 'a schedule',
                'schedule': {'scheduled_time': '2014-01-01T12:00:00'},
                'push': {
                    'audience': 'all',
                    'notification': {'alert': 'Hello'},
                    'device_types': 'all',
                    'options': {
                        'expiry': 10080
                    },
                    'message': {
                        'title': 'Title',
                        'body': 'Body',
                        'content_type': 'text/html',
                        'content_encoding': 'utf8',
                        'extra': {'more': 'stuff'},
                        'expiry': 10080,
                        'icons': {
                            'list_icon': 'http://cdn.example.com/message.png'
                        },
                        'options': {'some_delivery_option': 'true'},
                    },
                }
            }
        )

    def test_local_scheduled_payload(self):
        p = ua.Push(None)
        p.audience = ua.all_
        p.notification = ua.notification(alert='Hello')
        p.options = ua.options(10080)
        p.device_types = ua.all_
        p.message = ua.message(
            title='Title',
            body='Body',
            content_type='text/html',
            content_encoding='utf8',
        )

        sched = ua.ScheduledPush(None)
        sched.push = p
        sched.name = 'a schedule in device local time'
        sched.schedule = ua.local_scheduled_time(
            datetime.datetime(2015, 1, 1, 12, 0, 0)
        )

        self.assertEqual(sched.payload, {
            'name': 'a schedule in device local time',
            'schedule': {'local_scheduled_time': '2015-01-01T12:00:00'},
            'push': {
                'audience': 'all',
                'notification': {'alert': 'Hello'},
                'device_types': 'all',
                'options': {
                    'expiry': 10080
                },
                'message': {
                    'title': 'Title',
                    'body': 'Body',
                    'content_type': 'text/html',
                    'content_encoding': 'utf8'
                },
            }
        })

    def test_push_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'push_ids': [
                        '0492662a-1b52-4343-a1f9-c6b0c72931c0'
                    ]
                }
            ).encode('utf-8')
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
                pr.push_ids,
                ['0492662a-1b52-4343-a1f9-c6b0c72931c0']
            )

    def test_schedule_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'schedule_urls': [
                        (
                            'https://go.urbanairship.com/api/schedules/'
                            '0492662a-1b52-4343-a1f9-c6b0c72931c0'
                        )
                    ]
                }
            ).encode('utf-8')
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

            self.assertEquals(
                sched.url,
                (
                    'https://go.urbanairship.com/api/schedules/'
                    '0492662a-1b52-4343-a1f9-c6b0c72931c0'
                )
            )

    def test_local_schedule_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'schedule_urls': [
                        (
                            'https://go.urbanairship.com/api/schedules/'
                            '0492662a-1b52-4343-a1f9-c6b0c72931c0'
                        )
                    ]
                }
            ).encode('utf-8')
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

            self.assertEquals(
                sched.url,
                (
                    'https://go.urbanairship.com/api/schedules/'
                    '0492662a-1b52-4343-a1f9-c6b0c72931c0'
                )
            )

    def test_schedule_from_url(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'name': 'a schedule',
                'schedule': {'scheduled_time': '2013-07-15T18:40:20'},
                'push': {
                    'audience': 'all',
                    'notification': {'alert': 'Hello'},
                    'device_types': 'all',
                    'options': {'expiry': 10080},
                    'message': {
                        'title': 'Title',
                        'body': 'Body',
                        'content_type': 'text/html',
                        'content_encoding': 'utf8',
                    },
                },
            }).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            url = (
                'https://go.urbanairship.com/api/schedules/'
                '0492662a-1b52-4343-a1f9-c6b0c72931c0'
            )

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

            url = (
                'https://go.urbanairship.com/api/schedules/'
                '0492662a-1b52-4343-a1f9-c6b0c72931c0'
            )
            sched.url = url

            sched.cancel()

    def test_update_schedule(self):
        airship = ua.Airship('key', 'secret')
        sched = ua.ScheduledPush(airship)
        # Fail w/o URL
        self.assertRaises(ValueError, sched.update)

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            url = (
                'https://go.urbanairship.com/api/schedules/'
                '0492662a-1b52-4343-a1f9-c6b0c72931c0'
            )

            response = requests.Response()
            response.status_code = 202
            response._content = json.dumps(
                {
                    'schedule_urls':
                        [
                            (
                                'https://go.urbanairship.com/api/schedules/'
                                '0492662a-1b52-4343-a1f9-c6b0c72931c0'
                            )
                        ]
                }
            ).encode('utf-8')

            mock_request.return_value = response

            sched.url = url
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.device_types = ua.all_
            sched.push = push
            sched.schedule = ua.scheduled_time(datetime.datetime.now())

            sched.update()

    def test_options_int_expiry(self):
        opt = ua.options(expiry=10080)
        self.assertEqual(
            opt,
            {'expiry': 10080}
        )

    def test_options_date_expiry(self):
        opt = ua.options(expiry='2015-04-01T12:00:00')
        self.assertEqual(
            opt,
            {'expiry': '2015-04-01T12:00:00'}
        )

    def test_campaigns_list(self):
        cam = ua.campaigns(categories=['bugs', 'worms'])
        self.assertEqual(
            cam,
            {'categories': ['bugs', 'worms']}
        )

        with self.assertRaises(ValueError):
            ua.campaigns(categories=[])

        with self.assertRaises(TypeError):
            ua.campaigns({'categories': ['bugs', 'worms']})

    def test_campaigns_str(self):
        cam = ua.campaigns(categories='bugs')
        self.assertEqual(
            cam,
            {'categories': ['bugs']}
        )

        with self.assertRaises(ValueError):
            ua.campaigns(
                categories='''a_long_string_so_long_its_longer_than_
                                    sixty_four_characters_too_long'''
            )
