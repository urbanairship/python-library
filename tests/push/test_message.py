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
