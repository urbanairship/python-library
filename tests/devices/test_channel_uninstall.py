import unittest
import mock
import json
import requests
import urbanairship as ua


class TestChannelUninstall(unittest.TestCase):
    def test_channel_uninstall(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({'ok': True})
            mock_request.return_value = response
            airship = ua.Airship('key', 'secret')

            cu = ua.ChannelUninstall(airship)

            chans = [
                {
                    'channel_id': '01000001-01010000-01010000-01001100',
                    'device_type': 'ios'
                }
            ]

            cu_res = json.loads(cu.uninstall(chans).content)

            self.assertEqual(cu_res['ok'], True)