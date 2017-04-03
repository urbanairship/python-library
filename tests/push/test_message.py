import unittest

import urbanairship as ua


class TestMessage(unittest.TestCase):
    def test_simple_alert(self):
        self.assertEqual(
            ua.notification(
                alert='Hello'
            ),
            {
                'alert': 'Hello'
            }
        )

    def test_ios(self):
        self.assertEqual(
            ua.notification(
                ios=ua.ios(
                    alert='Hello',
                    badge='+1',
                    sound='cat.caf',
                    extra={'more': 'stuff'},
                    expiry='time',
                    category='test',
                    title='title',
                    subtitle='Subtitle',
                    mutable_content=True,
                    media_attachment={
                        'content': {
                            'title': 'Moustache Twirl',
                            'body': 'Have you ever seen a moustache like this?!'
                        },
                        'options': {
                            'crop': {
                                'height': 0.5,
                                'width': 0.5,
                                'x': 0.25,
                                'y': 0.25
                            },
                            'time': 15
                        },
                        'url': 'https://media.giphy.com/media/JYsWwF82EGnpC/giphy.gif'
                    },
                    interactive={
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes',
                            },
                            'no': {
                                'add_tag': 'clicked_no'
                            }
                        }
                    },
                    priority=10,
                    collapse_id='a'
                )
            ),
            {
                'ios': {
                    'alert': 'Hello',
                    'badge': '+1',
                    'sound': 'cat.caf',
                    'extra': {
                        'more': 'stuff',
                    },
                    'expiry': 'time',
                    'category': 'test',
                    'title': 'title',
                    'subtitle': 'Subtitle',
                    'mutable_content': True,
                    'media_attachment': {
                        'content': {
                            'title': 'Moustache Twirl',
                            'body': 'Have you ever seen a moustache like this?!'
                        },
                        'options': {
                            'crop': {
                                'height': 0.5,
                                'width': 0.5,
                                'x': 0.25,
                                'y': 0.25
                            },
                            'time': 15
                        },
                        'url': 'https://media.giphy.com/media/JYsWwF82EGnpC/giphy.gif'
                    },
                    'interactive': {
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes',
                            },
                            'no': {
                                'add_tag': 'clicked_no'
                            }
                        }
                    },
                    'priority': 10,
                    'collapse_id': 'a'
                }
            }
        )

        self.assertEqual(
            ua.notification(
                ios=ua.ios(
                    alert={
                        'foo': 'bar'
                    },
                    badge='+1',
                    sound='cat.caf',
                    extra={
                        'more': 'stuff'
                    },
                    category='test',
                    interactive={
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes'
                            },
                            'no': {
                                'add_tag': 'clicked_no'
                            }
                        }
                    },
                )
            ),
            {
                'ios': {
                    'alert': {'foo': 'bar'},
                    'badge': '+1',
                    'sound': 'cat.caf',
                    'extra': {
                        'more': 'stuff',
                    },
                    'category': 'test',
                    'interactive': {
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes'
                            },
                            'no': {
                                'add_tag': 'clicked_no'
                            }
                        }
                    }
                }
            }
        )

        self.assertEqual(
            ua.notification(
                ios=ua.ios(
                    content_available=True
                )
            ),
            {
                'ios': {
                    'content-available': True}
            }
        )

    def test_ios_unicode(self):
        self.assertEqual(
            ua.notification(
                ios=ua.ios(
                    alert=u'Hello',
                    badge=u'+1',
                    expiry=u'time',
                )
            ),
            {
                'ios': {
                    'alert': 'Hello',
                    'badge': '+1',
                    'expiry': 'time'
                }
            }
        )

        self.assertEqual(
            ua.notification(
                ios=ua.ios(
                    content_available=True
                )
            ),
            {
                'ios': {
                    'content-available': True
                }
            }
        )

    def test_android(self):
        self.assertEqual(
            ua.notification(
                android=ua.android(
                    alert='Hello',
                    delay_while_idle=True,
                    collapse_key='123456',
                    time_to_live=100,
                    extra={
                        'more': 'stuff'
                    },
                    interactive={
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes'
                            },
                            'no': {
                                'add_tag': 'clicked_no'
                            }
                        }
                    },
                    local_only=True,
                    wearable={
                        'background_image': 'http://example.com/background.png',
                        'extra_pages': [
                            {
                                'title': 'Page 1 title - optional title',
                                'alert': 'Page 1 title - optional alert'
                            },
                            {
                                'title': 'Page 2 title - optional title',
                                'alert': 'Page 2 title - optional alert'
                            }
                        ],
                        'interactive': {
                            'type': 'a_type',
                            'button_actions': {
                                'yes': {
                                    'add_tag': 'clicked_yes'
                                },
                                'no': {
                                    'add_tag': 'clicked_no'
                                }
                            }
                        }
                    },
                    delivery_priority='high',
                    style={
                        'type': 'big_picture',
                        'big_picture': 'bigpic.png',
                        'title': 'A title',
                        'summary': 'A summary'
                    },
                    title='A title',
                    summary='A summary',
                    sound='cowbell.mp3',
                    priority=-1,
                    category='alarm',
                    visibility=0,
                    public_notification={
                        'title': 'A title',
                        'alert': 'An alert',
                        'summary': 'A summary'
                    }
                )
            ),
            {
                'android': {
                    'alert': 'Hello',
                    'delay_while_idle': True,
                    'collapse_key': '123456',
                    'time_to_live': 100,
                    'extra': {
                        'more': 'stuff',
                    },
                    'interactive': {
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes'
                            },
                            'no': {
                                'add_tag': 'clicked_no'
                            }
                        }
                    },
                    'local_only': True,
                    'wearable': {
                        'background_image': 'http://example.com/background.png',
                        'extra_pages': [
                            {
                                'title': 'Page 1 title - optional title',
                                'alert': 'Page 1 title - optional alert'
                            },
                            {
                                'title': 'Page 2 title - optional title',
                                'alert': 'Page 2 title - optional alert'
                            }
                        ],
                        'interactive': {
                            'type': 'a_type',
                            'button_actions': {
                                'yes': {
                                    'add_tag': 'clicked_yes'
                                },
                                'no': {
                                    'add_tag': 'clicked_no'
                                }
                            }
                        }
                    },
                    'delivery_priority': 'high',
                    'style': {
                        'type': 'big_picture',
                        'big_picture': 'bigpic.png',
                        'title': 'A title',
                        'summary': 'A summary'
                    },
                    'title': 'A title',
                    'summary': 'A summary',
                    'sound': 'cowbell.mp3',
                    'priority': -1,
                    'category': 'alarm',
                    'visibility': 0,
                    'public_notification': {
                        'title': 'A title',
                        'alert': 'An alert',
                        'summary': 'A summary'
                    }
                }
            }
        )

    def test_android_unicode(self):
        self.assertEqual(
            ua.notification(
                android=ua.android(
                    alert=u'Hello',
                    time_to_live=u'100',
                )
            ),
            {
                'android': {
                    'alert': 'Hello',
                    'time_to_live': '100',
                }
            }
        )

    def test_amazon(self):
        self.assertEqual(
            ua.notification(
                amazon=ua.amazon(
                    alert='Amazon test',
                    title='My Title',
                    consolidation_key='123456',
                    expires_after=100,
                    summary='Summary of message',
                    extra={'more': 'stuff'},
                    interactive={
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes'
                            },
                            'no': {
                                'add_tag': 'clicked_no'
                            }
                        }
                    },
                    style={
                        'type': 'big_picture',
                        'big_picture': 'bigpic.png',
                        'title': 'A title',
                        'summary': 'A summary'
                    },
                    sound='cowbell.mp3'
                )
            ),
            {
                'amazon': {
                    'alert': 'Amazon test',
                    'title': 'My Title',
                    'consolidation_key': '123456',
                    'expires_after': 100,
                    'summary': 'Summary of message',
                    'extra': {
                        'more': 'stuff',
                    },
                    'interactive': {
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {
                                'add_tag': 'clicked_yes'
                            },
                            'no': {
                                'add_tag': 'clicked_no'
                            }
                        }
                    },
                    'style': {
                        'type': 'big_picture',
                        'big_picture': 'bigpic.png',
                        'title': 'A title',
                        'summary': 'A summary'
                    },
                    'sound': 'cowbell.mp3'
                }
            }
        )

    def test_amazon_unicode(self):
        self.assertEqual(
            ua.notification(
                amazon=ua.amazon(
                    alert=u'Amazon test',
                    expires_after=u'100',
                )
            ),
            {
                'amazon': {
                    'alert': 'Amazon test',
                    'expires_after': '100',
                }
            }
        )

    def test_wns_payload(self):
        self.assertEqual(
            ua.notification(
                wns=ua.wns_payload(
                    alert='Hello',
                )
            ),
            {
                'wns': {
                    'alert': 'Hello',
                }
            }
        )

        self.assertEqual(
            ua.notification(
                wns=ua.wns_payload(
                    toast={'key': 'value'},
                )
            ),
            {
                'wns': {
                    'toast': {'key': 'value'},
                }
            }
        )

        self.assertEqual(
            ua.notification(
                wns=ua.wns_payload(
                    tile={'key': 'value'},
                )
            ),
            {
                'wns': {
                    'tile': {'key': 'value'},
                }
            }
        )

        self.assertEqual(
            ua.notification(
                wns=ua.wns_payload(
                    badge={'key': 'Hello'},
                )
            ),
            {
                'wns': {
                    'badge': {'key': 'Hello'},
                }
            }
        )
        self.assertRaises(ValueError, ua.wns_payload, alert='Hello',
                          tile='Foo')

    def test_rich_push(self):
        self.assertEqual(
            ua.message(
                title='My Title',
                body='My Body',
                content_type='text/html',
                content_encoding='utf8',
                extra={
                    'more': 'stuff'
                },
                expiry='time'
            ),
            {
                'title': 'My Title',
                'body': 'My Body',
                'content_type': 'text/html',
                'content_encoding': 'utf8',
                'extra': {
                    'more': 'stuff'
                },
                'expiry': 'time'
            }
        )
        self.assertEqual(
            ua.message(
                title='My Title',
                body='My Body'),
            {
                'title': 'My Title',
                'body': 'My Body'
            }
        )

    def test_all_device_types(self):
        self.assertEqual(
            ua.device_types(
                ua.all_
            ),
            'all'
        )

    def options(self):
        airship = ua.Airship('key', 'secret')
        push = ua.Push(None)
        push.audience = ua.all_
        push.notification = ua.notification(alert='Hello Expiry')
        push.options = ua.options(expiry='2013-04-01T18:45:0')
        push.device_types = ua.all_

    def test_invalid_payloads(self):
        self.assertRaises(ValueError, ua.notification)

        self.assertRaises(
            ValueError,
            ua.ios,
            alert=100
        )
        self.assertRaises(
            ValueError,
            ua.ios,
            badge=object()
        )
        self.assertRaises(
            ValueError,
            ua.ios,
            badge='++100!'
        )
        self.assertRaises(
            ValueError,
            ua.ios,
            expiry=2.5
        )

    def test_interactive_missing_type(self):
        self.assertRaises(
            AttributeError,
            ua.interactive,
            type=None
        )

    def test_interactive_missing_button_actions(self):
        self.assertEqual(
            ua.interactive(
                type='a_type'
            ),
            {
                'type': 'a_type'
            }
        )

    def test_wearable(self):
        wearable = ua.wearable(
            background_image='http://example.com/background.png',
            extra_pages=[{'title': 'title', 'alert': 'wearable alert'}],
            interactive=ua.interactive(
                type='a_type',
                button_actions={'yes': {'add_tag': 'clicked_yes'}}
            )
        )


        self.assertEqual(
            ua.android(
                alert='android alert',
                local_only=False,
                wearable=wearable
            ),
            {
                'alert': 'android alert',
                'local_only': False,
                'wearable': {
                    'background_image': 'http://example.com/background.png',
                    'extra_pages': [
                        {'title': 'title', 'alert': 'wearable alert'}
                    ],
                    'interactive': {
                        'type': 'a_type',
                        'button_actions': {
                            'yes': {'add_tag': 'clicked_yes'}
                        }
                    }
                }
            }
        )

    def test_style(self):
        style = ua.style(
            style_type='big_picture',
            content='bigpic.png',
            title='A title',
            summary='A summary'
        )

        self.assertEqual(
            style,
            {
                'type': 'big_picture',
                'big_picture': 'bigpic.png',
                'title': 'A title',
                'summary': 'A summary'
            }
        )

    def test_public_notification(self):
        public_notification = ua.public_notification(
            alert='An alert',
            title='A title',
            summary='A summary'
        )

        self.assertEqual(
            public_notification,
            {
                'title': 'A title',
                'alert': 'An alert',
                'summary': 'A summary'
            }
        )
