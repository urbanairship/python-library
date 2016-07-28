import unittest

import mock
import requests

import wallet


CLIENT = wallet.Wallet('fake', 'client')


class PassApiTest(unittest.TestCase):

    @mock.patch.object(wallet.Wallet, '_request')
    def test_delete(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response

        wt = wallet.delete_pass(CLIENT, pass_id=12345)
        mock_request.assert_called_with(
            'DELETE',
            None,
            wallet.common.PASS_BASE_URL.format(12345),
            None,
            1.2,
            None
        )
        self.assertEqual(wt.status_code, 200)
