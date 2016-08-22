import json
import unittest
import mock
import requests

import wallet


class TemplateApiTest(unittest.TestCase):

    def setUp(self):
        self.client = wallet.Wallet('fake', 'creds')
        super(TemplateApiTest, self).setUp()

    @mock.patch.object(wallet.Wallet, '_request')
    def test_delete(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response

        wt = wallet.delete_template(self.client, template_id=12345)
        mock_request.assert_called_with(
            'DELETE',
            None,
            wallet.common.TEMPLATE_BASE_URL.format(12345),
            None,
            1.2,
            None
        )
        self.assertEqual(wt, True)

    @mock.patch.object(wallet.Wallet, '_request')
    def test_add_template_locations(self, mock_request):
        location = {
            "longitude": -122.374,
            "latitude": 37.618,
            "relevantText": "Hello loc0",
            "streetAddress1": "address line #1",
            "streetAddress2": "address line #2",
            "city": "Palo Alto",
            "region": "CA",
            "regionCode": "94404",
            "country": "US"
        }
        body = json.dumps({
            'locations': [location]
        })
        response = requests.Response()
        response._content = json.dumps([
            {
                'value': location,
                'locationId': 231,
                'fieldId': 312
            }
        ])
        mock_request.return_value = response

        wal = wallet.add_template_locations(
            self.client, [location], template_id=12345
        )
        mock_request.assert_called_with(
            'POST',
            body,
            wallet.common.TEMPLATE_ADD_LOCATION_URL.format(12345),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(wal[0]['value'], location)
        self.assertEqual(wal[0]['locationId'], 231)
        self.assertEqual(wal[0]['fieldId'], 312)

    @mock.patch.object(wallet.Wallet, '_request')
    def test_remove_template_location(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response

        wal = wallet.remove_template_location(
            self.client, 'location123', template_id=12345
        )
        mock_request.assert_called_with(
            'DELETE',
            None,
            wallet.common.TEMPLATE_REMOVE_LOCATION_URL.format(
                12345, 'location123'
            ),
            None,
            1.2,
            None
        )
        self.assertEqual(wal, True)

    @mock.patch.object(wallet.Wallet, '_request')
    def test_duplicate_template(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps(
            {'templateId': 54321}
        )
        mock_request.return_value = response
        wal = wallet.duplicate_template(self.client, template_id=12345)
        mock_request.assert_called_with(
            'POST',
            None,
            wallet.common.TEMPLATE_DUPLICATE_URL.format(12345),
            None,
            1.2,
            None
        )
        self.assertEqual(wal['templateId'], 54321)

    @mock.patch.object(wallet.Wallet, '_request')
    def test_listing(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        templates_json = json.dumps({
            'count': 133,
            'templateHeaders': [
                {
                   'vendor': 'Google',
                   'projectType': 'memberCard',
                   'projectId': '10057',
                   'type': 'Loyalty1',
                   'vendorId': '2',
                   'deleted': 'False',
                   'id': '23595',
                   'updatedAt': '2013-07-01T18:28:54.000Z',
                   'description': 'description',
                   'createdAt': '2013-07-01T18:28:54.000Z',
                   'name': 'New Wallet Template',
                   'disabled': 'False'
                },
                {
                   'vendor': 'Apple',
                   'projectType': 'memberCard',
                   'projectId': '10057',
                   'type': 'Store Card',
                   'vendorId': '1',
                   'deleted': 'False',
                   'id': '23593',
                   'updatedAt': '2013-07-01T18:28:33.000Z',
                   'description': 'Description',
                   'createdAt': '2013-07-01T18:28:33.000Z',
                   'name': 'Loyalty Card',
                   'disabled': 'False'
                }
            ],
            'pagination': {
                'order': 'id',
                'page': 1,
                'start': 0,
                'direction': 'DESC',
                'pageSize': 10
            }
        })
        response._content = templates_json
        mock_request.return_value = response

        listing_response = wallet.TemplateList(self.client)
        self.assertEqual(
            listing_response.next()['id'],
            '23595'
        )
        mock_request.assert_called_with(
            'GET',
            None,
            wallet.common.TEMPLATE_BASE_URL.format('headers'),
            None,
            1.2,
            {}
        )
