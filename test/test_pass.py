import datetime
import json
import unittest

import mock
import requests

import pass_builders
import uareach as ua
from uareach.passes import Pass


class PassApiTest(unittest.TestCase):

    def setUp(self):
        self.client = ua.Reach('fake', 'creds')
        super(PassApiTest, self).setUp()

    @mock.patch.object(ua.Reach, '_request')
    def test_delete(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response

        reach_response = ua.delete_pass(self.client, pass_id=12345)
        mock_request.assert_called_with(
            'DELETE',
            None,
            ua.common.PASS_BASE_URL.format(12345),
            None,
            1.2,
            None
        )
        self.assertEqual(reach_response, True)

    @mock.patch.object(ua.Reach, '_request')
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

        reach_response = ua.add_pass_locations(
            self.client, locations, pass_id=12345
        )
        mock_request.assert_called_with(
            'POST',
            body,
            ua.common.PASS_ADD_LOCATION_URL.format(12345),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(reach_response[0]['value'], locations[0])
        self.assertEqual(reach_response[0]['passLocationId'], 231)
        self.assertEqual(reach_response[1]['value'], locations[1])
        self.assertEqual(reach_response[1]['passLocationId'], 312)

    @mock.patch.object(ua.Reach, '_request')
    def test_delete_pass_location(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response

        reach_response = ua.delete_pass_location(
            self.client, 'location123', pass_id=12345
        )
        mock_request.assert_called_with(
            'DELETE',
            None,
            ua.common.PASS_DELETE_LOCATION_URL.format(
                12345, 'location123'
            ),
            None,
            1.2,
            None
        )

        self.assertEqual(reach_response, True)

    @mock.patch.object(ua.Reach, '_request')
    def test_get_pass(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        pass_json = json.dumps({
            'fields': {
                'Points': {
                    'fieldType': 'primary',
                    "numberStyle": 'numberStyleDecimal',
                    'value': 33.0
                }
            },
            'headers': {
                'barcode_encoding': {
                    'fieldType': 'barcode',
                    'formatType': 1,
                    'value': 'iso-8859-1'
                },
            },
            'id': '18971172',
            'templateId': '51234',
            'status': 'not_been_installed',
            'tags': []
        })
        response._content = pass_json
        mock_request.return_value = response
        pass_ = ua.get_pass(self.client, pass_id=12345)
        mock_request.assert_called_with(
            'GET',
            None,
            ua.common.PASS_BASE_URL.format(12345),
            None,
            1.2,
            None
        )

    def test_pass_dispatch(self):
        min_apple_json = {
            'fields': {
                'Points': {
                    'fieldType': 'primary',
                    "numberStyle": 'numberStyleDecimal',
                    'value': 33.0
                }
            }
        }
        apple_pass = ua.passes._pass_dispatch(min_apple_json)
        self.assertEquals(apple_pass.__class__.__name__, 'ApplePass')

        min_google_json = {
            'fields': {
                'Points': {
                    'fieldType': 'pointsModule',
                    'value': 33.0
                }
            }
        }
        google_pass = ua.passes._pass_dispatch(min_google_json)
        self.assertEquals(google_pass.__class__.__name__, 'GooglePass')

    @mock.patch.object(ua.Reach, '_request')
    def test_list_passes(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        pass_json = json.dumps({
            "count": 133,
            "passes":[
                {
                   "id":"12345",
                   "templateId":"12345",
                   "updatedAt":"2013-06-27T20:58:20.000Z",
                   "createdAt":"2013-06-27T20:58:18.000Z",
                   "serialNumber":"ff9db2ed-37aa-4691-a3b6-240108ac31f9",
                   "url":"https://wallet-api.urbanairship.com/v1/pass/1273/download"
                },
                {
                   "id":"12346",
                   "templateId":"12346",
                   "updatedAt":"2013-06-27T20:56:07.000Z",
                   "createdAt":"2013-06-27T20:56:03.000Z",
                   "serialNumber":"a2ea965a-0917-461d-ac67-749639831818",
                   "url":"https://wallet-api.urbanairship.com/v1/pass/1272/download"
                }
            ],
            "pagination":{
                "order": "id",
                "page": 1,
                "start": 0,
                "direction": "DESC",
                "pageSize": 2
            }
        })
        response._content = pass_json
        mock_request.return_value = response
        listing_response = ua.PassList(self.client)
        self.assertEqual(
            listing_response.next()['id'],
            '12345'
        )
        mock_request.assert_called_with(
            'GET',
            None,
            ua.common.PASS_BASE_URL.format(''),
            None,
            1.2,
            {}
        )


class PassTest(unittest.TestCase):

    def setUp(self):
        pass_ = Pass()
        member_name = ua.Field(
            name='Member Name',
            value='First Last'
        )
        pass_.add_fields(member_name)
        self.pass_ = pass_
        self.client = ua.Reach('fake', 'creds')

    @mock.patch.object(ua.Reach, '_request')
    def test_create_pass(self, mock_request):
        response = requests.Response()
        response._content = json.dumps({
            'url': 'https://wallet-api.urbanairship.com/v1/pass/123456/download',
            'id': '12345678'
        })
        response.status_code = 200
        mock_request.return_value = response
        payload = self.pass_._create_payload()
        create_response = self.pass_.create(self.client, template_id=54321)
        mock_request.assert_called_with(
            'POST',
            json.dumps(payload),
            ua.common.PASS_BASE_URL.format(54321),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(self.pass_.metadata['id'], '12345678')

    @mock.patch.object(ua.Reach, '_request')
    def test_update_pass(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps({'ticketId': 12345678})
        mock_request.return_value = response
        update_response = self.pass_.update(self.client, pass_id=12345)

        mock_request.assert_called_with(
            'PUT',
            json.dumps(self.pass_._create_payload()),
            ua.common.PASS_BASE_URL.format(12345),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(update_response['ticketId'], 12345678)

    def test_create_payload(self):
        pass_ = Pass()
        member_name = ua.Field(
            name='Member Name',
            value='Max Del Giudice'
        )
        member_id = ua.Field(
            name='Member ID',
            value=12345678
        )
        points = ua.Field(
            name='Points',
            value=5555
        )
        pass_.add_fields(member_name, member_id, points)
        pass_.add_headers(barcode_value='99999999')
        self.assertEqual(
            pass_._create_payload(),
            {
                'fields': {
                    'Member Name': {'value': 'Max Del Giudice'},
                    'Member ID': {'value': 12345678},
                    'Points': {'value': 5555}
                },
                'headers': {
                    'barcode_value': {
                        'fieldType': 'barcode',
                        'formatType': 'String',
                        'value': '99999999'
                    }
                }
            }
        )

    def test_set_public_url(self):
        self.pass_.set_public_url(type_='single')
        self.assertEqual(
            self.pass_._create_payload()['publicUrl'],
            {'type': 'single'}
        )
        self.pass_.set_public_url(type_='multiple')
        self.assertEqual(
            self.pass_._create_payload()['publicUrl'],
            {'type': 'multiple'}
        )
        self.assertRaises(
            ValueError, self.pass_.set_public_url, type_='none'
        )


class ApplePassTest(unittest.TestCase):

    def setUp(self):
        self.pass_ = pass_builders.build_apple_pass()
        self.client = ua.Reach('fake', 'creds')

    def test_add_remove_beacons(self):
        beacon = {
            'uuid': 'abcdef',
            'relevantText': "Here's a beacon",
            'major': 132,
            'minor': 32
        }

        self.pass_.add_beacon(
            'abcdef',
            relevant_text="Here's a beacon",
            major=132,
            minor=32
        )
        self.assertEqual(
            self.pass_._apple_features.beacons,
            [beacon]
        )

    def test_set_expiration(self):
        self.pass_.set_expiration(datetime.datetime(2014, 8, 6))
        json_payload = self.pass_._create_payload()
        self.assertEqual(len(json_payload['headers']), 2)
        self.assertEqual(
            json_payload['headers']['expirationDate'],
            {'value': '2014-08-06T00:00'}
        )

    def test_set_logo_image(self):
        self.pass_.set_logo_image('https://urbanairship.com/cool_image.png')
        self.assertEqual(
            self.pass_._create_payload()['headers']['logo_image'],
            {
                'value': 'https://urbanairship.com/cool_image.png',
                'fieldType': 'image',
                'formatType': 'String'
            }
        )

class GooglePassTest(unittest.TestCase):

    def setUp(self):
        self.pass_ = pass_builders.build_google_pass()
        self.client = ua.Reach('fake', 'creds')

    def test_set_expiration(self):
        self.pass_.set_expiration(datetime.datetime(2014, 8, 6))
        json_payload = self.pass_._create_payload()

        self.assertEqual(
            json_payload['fields']['endTime'],
            {
                'value': '2014-08-06T00:00'
            }
        )

    def test_field_json(self):
        view_json = {
            "Program Points": {
                "label": "UPDATED_LABEL",
                "value": "UPDATED_VALUE"
            },
            "Program Details": {
                "label": "UPDATED_LABEL",
                "value": "UPDATED_VALUE"
            },
            "Tier": {
                "label": "UPDATED_LABEL",
                "value": "UPDATED_VALUE"
            },
            "Merchant Website": {
                "label": "UPDATED_LABEL",
                "value": "UPDATED_VALUE"
            },
            "Loyalty Program Name": {
                "label": "UPDATED_LABEL",
                "value": "UPDATED_VALUE"
            }
        }

        program_points = ua.Field(name='Program Points', label='UPDATED_LABEL', value='UPDATED_VALUE')
        program_details = ua.Field(name='Program Details', label='UPDATED_LABEL', value='UPDATED_VALUE')
        tier = ua.Field(name='Tier', label='UPDATED_LABEL', value='UPDATED_VALUE')
        merchant_website = ua.Field(name='Merchant Website', label='UPDATED_LABEL', value='UPDATED_VALUE')
        program_name = ua.Field(name='Loyalty Program Name', label='UPDATED_LABEL', value='UPDATED_VALUE')
        self.pass_.set_fields(
            program_points, program_details, tier, merchant_website, program_name
        )

        self.assertEquals(self.pass_._create_payload()['fields'], view_json)
        self.assertEquals(self.pass_.view()['fields'], view_json)

    def test_set_offer(self):
        self.assertEqual(len(self.pass_._create_payload()['fields']), 1)
        offer_data = {
            'multiUserOffer': True,
            'redemptionChannel': 'both',
            'provider': 'UA'
        }
        self.pass_.set_offer(
            multi_user_offer=True,
            redemption_channel='both',
            provider='UA'
        )
        self.assertEqual(
            self.pass_._google_features.top_level_fields['offerModule'],
            offer_data
        )
        json_payload = self.pass_._create_payload()
        self.assertEqual(len(json_payload['fields']), 2)
        self.assertEqual(
            json_payload['fields']['offerModule'],
            offer_data
        )

    def test_set_logo_image(self):
        self.pass_.set_logo_image(
            'https://urbanairship.com/cool_image.png',
            description='The logo image'
        )
        self.assertEqual(
            self.pass_.view()['top_level_fields']['image'],
            {
                'title.string': 'https://urbanairship.com/cool_image.png',
                'description.string': 'The logo image'
            }
        )
        self.assertEqual(
            self.pass_._create_payload()['fields']['image'],
            {
                'title.string': 'https://urbanairship.com/cool_image.png',
                'description.string': 'The logo image'
            }
        )

    def test_set_background_image(self):
        self.pass_.set_background_image(
            value='https://urbanairship.com/cool_image.png',
            description='The background image'
        )
        self.assertEqual(
            self.pass_.view()['top_level_fields'][ua.GoogleFieldType._IMAGE_MODULE],
            {
                'image': 'https://urbanairship.com/cool_image.png',
                'imageDescription': 'The background image'
            }
        )
        self.assertEqual(
            self.pass_._create_payload()['fields'][ua.GoogleFieldType._IMAGE_MODULE],
            {
                'image': 'https://urbanairship.com/cool_image.png',
                'imageDescription': 'The background image'
            }
        )

    def test_add_message(self):
        self.pass_.add_message(
            body='The message body',
            header='The message title',
            action_uri='https://urbanairship.com',
            action_uri_description='Cool website',
            image_uri='https://urbanairship.com/cool_image.png',
            image_description='Cool image',
            starttime=datetime.datetime(2016, 9, 15),
            endtime=datetime.datetime(2016, 10, 15),
        )

        # Test full example
        self.assertEqual(
            self.pass_._create_payload()['messages'][0],
            {
                'body': 'The message body',
                'header': 'The message title',
                'actionUri': 'https://urbanairship.com',
                'actionUriDescription': 'Cool website',
                'imageUri': 'https://urbanairship.com/cool_image.png',
                'imageDescription': 'Cool image',
                'startTime': '2016-09-15T00:00',
                'endTime': '2016-10-15T00:00'
            }
        )

        self.assertRaises(
            ValueError, self.pass_.add_message, header='A header, but no body!'
        )
