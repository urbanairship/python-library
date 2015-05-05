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
                    }
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
                    }
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
                    }
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
                    }
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

    def test_blackberry(self):
        self.assertEqual(
            ua.notification(
                blackberry=ua.blackberry(
                    alert='Hello',
                )
            ),
            {
                'blackberry': {
                    'body': 'Hello',
                    'content_type': 'text/plain',
                }
            }
        )

        self.assertEqual(
            ua.notification(
                blackberry=ua.blackberry(
                    body='Hello',
                    content_type='text/html',
                )
            ),
            {
                'blackberry': {
                    'body': 'Hello',
                    'content_type': 'text/html',
                }
            }
        )
        self.assertRaises(
            ValueError,
            ua.blackberry,
            body='Hello'
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

    def test_mpns_payload(self):
        self.assertEqual(
            ua.notification(
                mpns=ua.mpns_payload(
                    alert='Hello',
                )
            ),
            {
                'mpns': {
                    'alert': 'Hello',
                }
            }
        )

        self.assertEqual(
            ua.notification(
                mpns=ua.mpns_payload(
                    toast={
                        'key': 'Hello'
                    },
                )
            ),
            {
                'mpns': {
                    'toast': {
                        'key': 'Hello'
                    },
                }
            }
        )

        self.assertEqual(
            ua.notification(
                mpns=ua.mpns_payload(
                    tile={
                        'key': 'Hello'
                    },
                )
            ),
            {
                'mpns': {
                    'tile': {
                        'key': 'Hello'
                    },
                }
            }
        )

        self.assertRaises(
            ValueError,
            ua.mpns_payload,
            alert='Hello',
            tile='Foo'
        )

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
        self.assertEqual(
            ua.android(
                alert='android alert',
                local_only=False,
                wearable={
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