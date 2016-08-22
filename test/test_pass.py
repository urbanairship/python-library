import unittest
import json

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

        wal = wallet.delete_pass(CLIENT, pass_id=12345)
        mock_request.assert_called_with(
            'DELETE',
            None,
            wallet.common.PASS_BASE_URL.format(12345),
            None,
            1.2,
            None
        )
        self.assertEqual(wal, True)

    @mock.patch.object(wallet.Wallet, '_request')
    def test_add_pass_locations(self, mock_request):
        locations = [
            {
                "longitude": -122.374,
                "latitude": 37.618,
                "relevantText": "Hello loc0",
                "streetAddress1": "address line #1",
                "streetAddress2": "address line #2",
                "city": "Palo Alto",
                "region": "CA",
                "regionCode": "94404",
                "country": "US"
            },
            {
                "longitude": -122.374,
                "latitude": 37.618,
                "relevantText": "Hello loc0",
                "streetAddress1": "address line #1",
                "streetAddress2": "address line #2",
                "city": "Palo Alto",
                "region": "CA",
                "regionCode": "94405",
                "country": "US"
            }
        ]
        body = json.dumps({
            'locations': locations
        })
        response = requests.Response()
        response._content = json.dumps([
            {
                'value': locations[0],
                'passLocationId': 231
            },
            {
                'value': locations[1],
                'passLocationId': 312
            }
        ])
        mock_request.return_value = response

        wal = wallet.add_pass_locations(
            CLIENT, locations, pass_id=12345
        )
        mock_request.assert_called_with(
            'POST',
            body,
            wallet.common.PASS_ADD_LOCATION_URL.format(12345),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(wal[0]['value'], locations[0])
        self.assertEqual(wal[0]['passLocationId'], 231)
        self.assertEqual(wal[1]['value'], locations[1])
        self.assertEqual(wal[1]['passLocationId'], 312)

    @mock.patch.object(wallet.Wallet, '_request')
    def test_delete_pass_location(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response

        wal = wallet.delete_pass_location(
            CLIENT, 'location123', pass_id=12345
        )
        mock_request.assert_called_with(
            'DELETE',
            None,
            wallet.common.PASS_DELETE_LOCATION_URL.format(
                12345, 'location123'
            ),
            None,
            1.2,
            None
        )

        self.assertEqual(wal, True)
