from collections import defaultdict
import datetime
import json
import mock
import requests
import unittest

import uareach as ua
from uareach import common
from uareach.templates import Template
from template_builders import build_apple_loyalty, build_google_loyalty


class TemplateApiTest(unittest.TestCase):

    def setUp(self):
        self.client = ua.Reach('fake', 'creds')
        super(TemplateApiTest, self).setUp()

    @mock.patch.object(ua.Reach, '_request')
    def test_delete(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response

        reach_response = ua.delete_template(self.client, template_id=12345)
        mock_request.assert_called_with(
            'DELETE',
            None,
            common.TEMPLATE_BASE_URL.format(12345),
            None,
            1.2,
            None
        )

        self.assertEqual(reach_response, True)

    @mock.patch.object(ua.Reach, '_request')
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

        reach_response = ua.add_template_locations(
            self.client, [location], template_id=12345
        )
        mock_request.assert_called_with(
            'POST',
            body,
            ua.common.TEMPLATE_ADD_LOCATION_URL.format(12345),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(reach_response[0]['value'], location)
        self.assertEqual(reach_response[0]['locationId'], 231)
        self.assertEqual(reach_response[0]['fieldId'], 312)

    @mock.patch.object(ua.Reach, '_request')
    def test_remove_template_location(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response

        reach_response = ua.delete_template_location(
            self.client, 'location123', template_id=12345
        )
        mock_request.assert_called_with(
            'DELETE',
            None,
            common.TEMPLATE_REMOVE_LOCATION_URL.format(12345, 'location123'),
            None,
            1.2,
            None
        )
        self.assertEqual(reach_response, True)

    @mock.patch.object(ua.Reach, '_request')
    def test_duplicate_template(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps(
            {'templateId': 54321}
        )
        mock_request.return_value = response
        reach_response = ua.duplicate_template(self.client, template_id=12345)
        mock_request.assert_called_with(
            'POST',
            None,
            ua.common.TEMPLATE_DUPLICATE_URL.format(12345),
            None,
            1.2,
            None
        )
        self.assertEqual(reach_response['templateId'], 54321)

    @mock.patch.object(ua.Reach, '_request')
    def test_get_apple_template(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        template_json = json.dumps({
            'fieldsModel': {
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
                        'formatType': 'String',
                        'value': 'iso-8859-1'
                    },
                }
            },
            'templateHeader': {
                'description': 'Hello',
                'name': 'Test',
                'type': 'Loyalty',
                'vendor': 'Apple',
                'vendorId': 1
            }
        })
        response._content = template_json
        mock_request.return_value = response
        ua.get_template(self.client, template_id=12345)
        mock_request.assert_called_with(
            'GET',
            None,
            common.TEMPLATE_BASE_URL.format(12345),
            None,
            1.2,
            None
        )

    @mock.patch.object(ua.Reach, '_request')
    def test_get_google_template(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        template_json = json.dumps({
            'fieldsModel': {
                'infoModuleData': {
                    'backgroundColor': {
                        'formatType': 'String',
                        'fieldType': 'infoModuleData',
                        'value': 339
                    }
                }
            },
            'headers': {
                'barcode_encoding': {
                    'fieldType': 'topLevel',
                    'formatType': 'String',
                    'value': 'iso-8859-1',
                    'label': '',
                },
            },
            'templateHeader': {
                'vendor': 'Google',
                'projectType': "memberCard",
                'projectId': 3456,
                'description': 'Hello',
                'type': 'Loyalty',
                'vendorId': 2,
                'name': 'Test'
            }
        })
        response._content = template_json
        mock_request.return_value = response
        ua.get_template(self.client, template_id=67890)
        mock_request.assert_called_with(
            'GET',
            None,
            ua.common.TEMPLATE_BASE_URL.format(67890),
            None,
            1.2,
            None
        )

    @mock.patch.object(ua.Reach, '_request')
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
                   'name': 'New Reach Template',
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
        listing_response = ua.TemplateList(self.client)
        self.assertEqual(
            listing_response.next()['id'],
            '23595'
        )
        mock_request.assert_called_with(
            'GET',
            None,
            common.TEMPLATE_BASE_URL.format('headers'),
            None,
            1.2,
            {}
        )


class TemplateTest(unittest.TestCase):

    def setUp(self):
        self.template = Template()
        self.template.add_metadata(name='Test generic template')

    def test_add_fields(self):
        member_name = ua.Field(
            name='Member Name',
            label='Member Name',
            value='First Last',
            fieldType=ua.AppleFieldType.PRIMARY
        )
        merchant_website = ua.Field(
            name='Merchant Website',
            label='Merchant Website',
            value='http://test.com',
            fieldType=ua.AppleFieldType.BACK
        )
        self.template.add_fields(member_name, merchant_website)
        self.assertEqual(self.template.fields['Member Name'], member_name)
        self.assertEqual(
            self.template.fields['Merchant Website'], merchant_website
                         )

    def test_remove_fields(self):
        member_name = ua.Field(
            name='Member Name',
            label='Member Name',
            value='First Last',
            fieldType=ua.AppleFieldType.PRIMARY
        )
        merchant_website = ua.Field(
            name='Merchant Website',
            label='Merchant Website',
            value='http://test.com',
            fieldType=ua.AppleFieldType.BACK
        )
        self.template.add_fields(member_name, merchant_website)
        self.assertNotEqual(self.template.fields, defaultdict(dict))
        self.template.remove_fields('Member Name', 'Merchant Website')
        self.assertEqual(self.template.fields, defaultdict(dict))

    def test_set_fields(self):
        member_name = ua.Field(
            name='Member Name',
            label='Member Name',
            value='First Last',
            fieldType=ua.AppleFieldType.PRIMARY
        )
        merchant_website = ua.Field(
            name='Merchant Website',
            label='Merchant Website',
            value='http://test.com',
            fieldType=ua.AppleFieldType.BACK
        )
        self.template.add_fields(member_name, merchant_website)
        self.assertNotEqual(self.template.fields, defaultdict(dict))
        points = ua.Field(
            name='Reward Points',
            label='Reward Points',
            value=1234.0,
            fieldType=ua.AppleFieldType.SECONDARY
        )
        self.template.set_fields(points)
        self.assertEqual(len(self.template.fields), 1)
        self.assertEqual(self.template.fields['Reward Points'], points)

    def test_add_metadata(self):
        self.template.add_metadata(
            description='a description!',
            vendorId=1,
            vendor='Apple'
        )
        self.assertEqual(
            self.template.metadata['description'], 'a description!'
        )
        self.assertEqual(self.template.metadata['vendorId'], 1)
        self.assertEqual(self.template.metadata['vendor'], 'Apple')

    def test_remove_metadata(self):
        self.template.add_metadata(
            description='a description!',
            vendorId=1,
            vendor='Apple'
        )
        self.assertEqual(len(self.template.metadata), 4)
        self.template.remove_metadata('vendorId', 'vendor')
        self.assertEqual(len(self.template.metadata), 2)
        self.assertIsNone(self.template.metadata.get('vendorId', None))
        self.assertIsNone(self.template.metadata.get('vendor', None))

    def test_set_metadata(self):
        self.template.add_metadata(
            description='a description!',
            vendorId=1,
            vendor='Apple'
        )
        self.assertEqual(len(self.template.metadata), 4)
        self.template.set_metadata(
            name='new name!!',
            description='new description',
            vendorId=2,
            vendor='Google'
        )
        self.assertEqual(
            self.template.metadata,
            {
                'name': 'new name!!',
                'description': 'new description',
                'vendorId': 2,
                'vendor': 'Google'
            }
        )

    def test_add_header(self):
        self.template.add_metadata(vendor='Apple')
        self.template.add_header('barcode_value', '123456789')
        self.template.add_header('logo_color', ua.rgb(23, 23, 23))
        self.assertEqual(
            self.template.headers['barcode_value'],
            {'value': '123456789', 'fieldType': 'barcode', 'formatType': 'String'}
        )
        self.assertEqual(
            self.template.headers['logo_color'],
            {
                'value': 'rgb(23,23,23)',
                'fieldType': 'topLevel',
                'formatType': 'String'
            }
        )
        self.assertRaises(
            ValueError,
            lambda: self.template.add_header('non_existent_header', 'blah')
        )

    def test_add_headers(self):
        self.template.add_metadata(vendor='Apple')
        self.template.add_headers(
            barcode_value='123456789',
            logo_color=ua.rgb(23, 23, 23)
        )
        self.assertEqual(
            self.template.headers,
            {
                'barcode_value': {
                    'value': '123456789',
                    'fieldType': 'barcode',
                    'formatType': 'String'
                },
                'logo_color': {
                    'value': 'rgb(23,23,23)',
                    'fieldType': 'topLevel',
                    'formatType': 'String'
                }
            }
        )

    def test_remove_headers(self):
        self.template.add_metadata(vendor='Apple')
        self.template.add_headers(
            barcode_value='123456789',
            logo_color=ua.rgb(23, 23, 23)
        )
        self.assertNotEqual(self.template.headers, {})
        self.template.remove_headers('barcode_value', 'logo_color')
        self.assertEqual(self.template.headers, {})

    def test_set_headers(self):
        self.template.add_metadata(vendor='Apple')
        self.template.add_headers(
            barcode_value='123456789',
            logo_color=ua.rgb(23, 23, 23)
        )
        self.assertNotEqual(self.template.headers, {})
        self.template.set_headers(
            background_color=ua.rgb(0, 147, 201),
            logo_text='logo text',
            thumbnail_image='https://google.com/images/cool_gif_bro.gif'
        )
        self.assertEqual(
            self.template.headers,
            {
                'background_color': {
                    'value': 'rgb(0,147,201)',
                    'fieldType': 'topLevel',
                    'formatType': 'String'
                },
                'logo_text': {
                    'value': 'logo text',
                    'fieldType': 'topLevel',
                    'formatType': 'String'
                },
                'thumbnail_image': {
                    'value': 'https://google.com/images/cool_gif_bro.gif',
                    'fieldType': 'image',
                    'formatType': 'String'
                }
            }
        )

    def test_build_url(self):
        # Lookup template URLs
        get_template_url = Template.build_url(
            common.TEMPLATE_BASE_URL, main_id=1234
        )
        self.assertEqual(
            get_template_url, common.TEMPLATE_BASE_URL.format(1234)
        )
        get_template_url = Template.build_url(
            common.TEMPLATE_BASE_URL, external_id=1234
        )
        self.assertEqual(
            get_template_url, common.TEMPLATE_BASE_URL.format('id/1234')
        )
        # Create template URLs
        create_template_url = Template.build_url(
            common.TEMPLATE_BASE_URL, main_id=1234
        )
        self.assertEqual(
            create_template_url, common.TEMPLATE_BASE_URL.format(1234)
        )
        create_template_url = Template.build_url(
            common.TEMPLATE_BASE_URL, main_id=1234, external_id=5678
        )
        self.assertEqual(
            create_template_url,
            common.TEMPLATE_BASE_URL.format('1234/id/5678')
        )
        # Delete template URLs
        delete_template_url = Template.build_url(
            common.TEMPLATE_BASE_URL, main_id=1234
        )
        self.assertEqual(
            delete_template_url, common.TEMPLATE_BASE_URL.format(1234)
        )
        delete_template_url = Template.build_url(
            common.TEMPLATE_BASE_URL, external_id=1234
                                               )
        self.assertEqual(
            delete_template_url, common.TEMPLATE_BASE_URL.format('id/1234')
        )
        # Duplicate template URLs
        duplicate_url = Template.build_url(
            common.TEMPLATE_DUPLICATE_URL, main_id=1234
        )
        self.assertEqual(
            duplicate_url, common.TEMPLATE_DUPLICATE_URL.format(1234)
        )
        duplicate_url = Template.build_url(
            common.TEMPLATE_DUPLICATE_URL, external_id=1234
        )
        self.assertEqual(
            duplicate_url, common.TEMPLATE_DUPLICATE_URL.format('id/1234')
        )
        # Add template location URLs
        add_location_url = Template.build_url(
            common.TEMPLATE_ADD_LOCATION_URL, main_id=1234
                                            )
        self.assertEqual(
            add_location_url, common.TEMPLATE_ADD_LOCATION_URL.format(1234)
        )
        add_location_url = Template.build_url(
            common.TEMPLATE_ADD_LOCATION_URL, external_id=1234
                                            )
        self.assertEqual(
            add_location_url,
            common.TEMPLATE_ADD_LOCATION_URL.format('id/1234')
        )
        # Remove template location URLs
        rem_location_url = Template.build_url(
            common.TEMPLATE_REMOVE_LOCATION_URL,
            main_id=1234,
            location_id=5678
        )
        self.assertEqual(
            rem_location_url,
            common.TEMPLATE_REMOVE_LOCATION_URL.format(1234, 5678)
        )
        rem_location_url = Template.build_url(
            common.TEMPLATE_REMOVE_LOCATION_URL,
            external_id=1234,
            location_id=5678
        )
        self.assertEqual(
            rem_location_url,
            common.TEMPLATE_REMOVE_LOCATION_URL.format('id/1234', 5678)
        )


class AppleTemplateTest(unittest.TestCase):

    def setUp(self):
        self.template = build_apple_loyalty()
        self.client = ua.Reach('fake', 'creds')
        super(AppleTemplateTest, self).setUp()

    @mock.patch.object(ua.Reach, '_request')
    def test_create_template(self, mock_request):
        response = requests.Response()
        response._content = json.dumps({'templateId': 54123})
        response.status_code = 200
        mock_request.return_value = response

        create_response = self.template.create(self.client, project_id=12345)
        mock_request.assert_called_with(
            'POST',
            json.dumps(self.template._create_payload()),
            common.TEMPLATE_BASE_URL.format(12345),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(create_response['templateId'], 54123)

    @mock.patch.object(ua.Reach, '_request')
    def test_update_template(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response
        # self.template.add_metadata(id_=12345)

        update_response = self.template.update(self.client, template_id=12345)
        mock_request.assert_called_with(
            'PUT',
            json.dumps(self.template._create_payload()),
            common.TEMPLATE_BASE_URL.format(12345),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(update_response, True)

    def test_add_header(self):
        self.assertEqual(
            self.template.headers['barcode_type']['value'],
            ua.BarcodeType.convert_to_apple(ua.BarcodeType.PDF_417)
        )

        # Check barcode validation
        self.assertRaises(
            ValueError,
            lambda: self.template.add_headers(barcode_type=ua.BarcodeType.EAN_13)
        )

    # Add another test outside of the test_update_template?
    def test_add_metadata(self):
        pass

    def test_add_beacon(self):
        self.template.add_beacon(
            'f7c7066e-ef28-4679-87c5-df3686a3dddb',
            relevant_text='Hello new beacon'
        )
        self.assertEqual(len(self.template.beacons), 2)
        for beacon in self.template.beacons:
            if beacon['uuid'] == 'f7c7066e-ef28-4679-87c5-df3686a3dddb':
                self.assertEqual(beacon['relevantText'], 'Hello new beacon')

    def test_remove_beacon(self):
        self.template.remove_beacon('3526dee6-4ea8-11e6-beb8-9e71128cae77')
        self.assertEqual(self.template.beacons, [])


class GoogleTemplateTest(unittest.TestCase):

    def setUp(self):
        self.template = build_google_loyalty()
        self.client = ua.Reach('fake', 'creds')
        super(GoogleTemplateTest, self).setUp()

    @mock.patch.object(ua.Reach, '_request')
    def test_create_template(self, mock_request):
        response = requests.Response()
        response._content = json.dumps({'templateId': 54321})
        response.status_code = 200
        mock_request.return_value = response

        create_response = self.template.create(self.client, project_id=12345)
        mock_request.assert_called_with(
            'POST',
            json.dumps(self.template._create_payload()),
            common.TEMPLATE_BASE_URL.format(12345),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(create_response['templateId'], 54321)

    @mock.patch.object(ua.Reach, '_request')
    def test_update_template(self, mock_request):
        response = requests.Response()
        response.status_code = 200
        mock_request.return_value = response
        # self.template.add_metadata(id_=12345)

        update_response = self.template.update(self.client, template_id=54321)
        mock_request.assert_called_with(
            'PUT',
            json.dumps(self.template._create_payload()),
            common.TEMPLATE_BASE_URL.format(54321),
            'application/json',
            1.2,
            None
        )
        self.assertEqual(update_response, True)

        # Add another test outside of the test_update_template?
        def test_add_metadata(self):
            pass

    def test_add_header(self):
        self.assertEqual(
            self.template.headers['barcode_type']['value'],
            ua.BarcodeType.PDF_417
        )

        self.template.add_headers(
            barcode_type=ua.BarcodeType.AZTEC
        )
        self.assertEqual(
            self.template.headers['barcode_type']['value'],
            ua.BarcodeType.AZTEC
        )
        self.assertRaises(
            ValueError,
            lambda: self.template.add_headers(logo_color=ua.rgb(12, 12, 12))
        )

    def test_add_top_level_fields(self):
        self.template.add_top_level_fields(
            ua.GoogleFieldType.TITLE_MODULE,
            image='https://s3.amazonaws.com/passtools_prod/1/images/default-loyalty-logo.png',
            imageDescription='An image!'
        )
        payload = self.template._create_payload()
        self.assertEqual(
            payload[ua.GoogleFieldType.TITLE_MODULE]['image'],
            'https://s3.amazonaws.com/passtools_prod/1/images/default-loyalty-logo.png'
        )
        self.assertEqual(
            payload[ua.GoogleFieldType.TITLE_MODULE]['imageDescription'],
            'An image!'
        )

    def test_set_logo_image(self):
        self.template.set_logo_image(
            'https://imgur.com/cool_image.png', description='Image'
        )
        payload = self.template._create_payload()
        self.assertEqual(
            payload[ua.GoogleFieldType.TITLE_MODULE]['image'],
            'https://imgur.com/cool_image.png'
        )

    def test_set_background_image(self):
        self.template.set_background_image(
            'https://imgur.com/cool_image.png',
            description='Super cool image'
        )
        payload = self.template._create_payload()
        self.assertEqual(
            payload[ua.GoogleFieldType._IMAGE_MODULE]['image'],
            'https://imgur.com/cool_image.png'
        )

    def test_set_offer(self):
        date = datetime.datetime(2017,1,31)
        offer_json = {
            'multiUserOffer': False,
            'redemptionChannel': 'both',
            'provider': 'The provider',
            'endTime': '2017-01-31T00:00'
        }
        self.template.set_offer(
            multi_user_offer=False,
            redemption_channel='both',
            provider='The provider',
            endtime=date
        )

        self.assertEqual(
            self.template.top_level_fields[ua.GoogleFieldType._OFFER_MODULE],
            offer_json
        )

    def test_add_message(self):
        # Test error
        self.assertRaises(
            ValueError,
            lambda: self.template.add_message(header="There's no body here!")
        )

        # Test minimal
        self.template.add_message(body='Test body')
        payload = self.template._create_payload()
        self.assertEqual(payload['messages'][0]['body'], 'Test body')

        # Test additional non-minimal message
        self.template.add_message(
            header='A title',
            body='Test body',
            action_uri='https://urbanairship.com'
        )
        payload = self.template._create_payload()
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(payload['messages'][1]['header'], 'A title')

    def test_process_module_data(self):
        temp = ua.GoogleTemplate()
        module_data = {
            'Program Points': {
                'balance': 250,
                'label': 'Program Points',
                'hideEmpty': False,
                'formatType': 'Number',
                'fieldType': 'loyaltyPoints',
                'order': 1
            },
            'Tier': {
                'balance':  '2.0',
                'label': 'Tier',
                'hideEmpty': False,
                'formatType': 'Number',
                'fieldType': 'pointsModule',
                'order': 2
            }
        }

        program_points = ua.Field(
            name='Program Points',
            label='Program Points',
            value=250,
            hideEmpty=False,
            formatType='Number',
            fieldType=ua.GoogleFieldType.POINTS_MODULE,
            order=1
        )

        tier = ua.Field(
            name='Tier',
            label='Tier',
            value='2.0',
            hideEmpty=False,
            formatType='Number',
            fieldType=ua.GoogleFieldType.POINTS_MODULE,
            order=2
        )

        temp._process_module_data(ua.GoogleFieldType.POINTS_MODULE, module_data)
        self.assertTrue(temp.fields['Program Points'] == program_points)
        self.assertTrue(temp.fields['Tier'] == tier)

    def test_handle_reserved_names(self):
        temp = ua.GoogleTemplate()
        image_special = {
            'title.string': 'https://www.google.com',
            'hideEmpty': False,
            'formatType': 'String',
            'fieldType': 'titleModule',
            'description.string': ''
        }

        temp._handle_reserved_names(
            ua.GoogleFieldType.TITLE_MODULE,
            'image',
            image_special
        )

        self.assertEqual(
            temp.top_level_fields[ua.GoogleFieldType.TITLE_MODULE]['image'],
            'https://www.google.com'
        )
