import unittest

import urbanairship as ua


class TestMessage(unittest.TestCase):

    def test_simple_alert(self):
        self.assertEqual(
            ua.notification(alert='Hello'),
            {'alert': 'Hello'})

    def test_ios(self):
        self.assertEqual(
            ua.notification(ios=ua.ios(
                alert='Hello',
                badge='+1',
                sound='cat.caf',
                extra={'more': 'stuff'}
            )),
            {'ios': {
                'alert': 'Hello',
                'badge': '+1',
                'sound': 'cat.caf',
                'extra': {
                    'more': 'stuff',
                }
            }})

    def test_android(self):
        self.assertEqual(
            ua.notification(android=ua.android(
                alert='Hello',
                delay_while_idle=True,
                extra={'more': 'stuff'}
            )),
            {'android': {
                'alert': 'Hello',
                'delay_while_idle': True,
                'extra': {
                    'more': 'stuff',
                }
            }})

    def test_blackberry(self):
        self.assertEqual(
            ua.notification(blackberry=ua.blackberry(
                alert='Hello',
            )),
            {'blackberry': {
                'body': 'Hello',
                'content_type': 'text/plain',
            }})

        self.assertEqual(
            ua.notification(blackberry=ua.blackberry(
                body='Hello', content_type='text/html',
            )),
            {'blackberry': {
                'body': 'Hello',
                'content_type': 'text/html',
            }})
        self.assertRaises(ValueError, ua.blackberry, body='Hello')

    def test_wns_payload(self):
        self.assertEqual(
            ua.notification(wns=ua.wns_payload(
                alert='Hello',
            )),
            {'wns': {
                'alert': 'Hello',
            }})

        self.assertEqual(
            ua.notification(wns=ua.wns_payload(
                toast={'key': 'Hello'},
            )),
            {'wns': {
                'toast': {'key': 'Hello'},
            }})
        self.assertRaises(ValueError, ua.wns_payload, alert='Hello',
            tile='Foo')

    def test_mpns_payload(self):
        self.assertEqual(
            ua.notification(mpns=ua.mpns_payload(
                alert='Hello',
            )),
            {'mpns': {
                'alert': 'Hello',
            }})

        self.assertEqual(
            ua.notification(mpns=ua.mpns_payload(
                toast={'key': 'Hello'},
            )),
            {'mpns': {
                'toast': {'key': 'Hello'},
            }})
        self.assertRaises(ValueError, ua.mpns_payload, alert='Hello',
            tile='Foo')
