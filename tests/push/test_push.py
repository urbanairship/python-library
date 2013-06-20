import unittest

import mock

import urbanairship as ua


class TestPush(unittest.TestCase):

    def test_push_success(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            mock_request.return_value = (202,
                '''{"push_ids": ["0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')

            airship = ua.Airship('key', 'secret')
            push = airship.create_push()
            push.audience = ua.all_
            push.notification = ua.notification(alert='Hello')
            push.device_types = ua.all_
            push.send()
