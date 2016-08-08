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
                   'id':'23593',
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
