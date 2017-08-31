import datetime
import json
import mock
import requests
import unittest

import urbanairship as ua


class TestTemplatePush(unittest.TestCase):
    def test_full_payload(self):
        p = ua.TemplatePush(None)
        p.audience = ua.ios_channel('b8f9b663-0a3b-cf45-587a-be880946e881')
        p.device_types = ua.device_types('ios')
        p.merge_data = ua.merge_data(
            template_id='ef34a8d9-0ad7-491c-86b0-aea74da15161',
            substitutions={
                'FIRST_NAME': 'Bob',
                'LAST_NAME': 'Smith',
                'TITLE': ''
            }
        )

        self.assertEqual(
            p.payload,
            {
                'device_types': ['ios'],
                'merge_data': {
                    'template_id': 'ef34a8d9-0ad7-491c-86b0-aea74da15161',
                    'substitutions': {
                        'FIRST_NAME': 'Bob',
                        'LAST_NAME': 'Smith',
                        'TITLE': ''
                    }
                },
                'audience': {
                    'ios_channel': 'b8f9b663-0a3b-cf45-587a-be880946e881'
                }
            }
        )


class TestTemplate(unittest.TestCase):
    def test_template_lookup(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'id': 'ef34a8d9-0ad7-491c-86b0-aea74da15161',
                    'created_at': '2017-08-30T23:04:54.014Z',
                    'modified_at': '2017-08-31T00:02:41.493Z',
                    'last_used': None,
                    'name': 'Welcome Message',
                    'description': 'Our welcome message',
                    'variables': [
                        {
                            'key': 'TITLE',
                            'name': 'Title',
                            'description': 'e.g. Mr, Ms, Dr, etc.',
                            'default_value': ''
                        },
                        {
                            'key': 'FIRST_NAME',
                            'name': 'First Name',
                            'description': 'Given name',
                            'default_value': None
                        },
                        {
                            'key': 'LAST_NAME',
                            'name': 'Last Name',
                            'description': 'Family name',
                            'default_value': None
                        }
                    ],
                    'push': {
                        'notification': {
                            'alert': 'Hello {{FIRST_NAME}}, this is your'
                                     'welcome message!'
                        }
                    }
                }
            ).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

        airship = ua.Airship('key', 'secret')
        template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'
        template_lookup = ua.Template.lookup(airship, template_id)

        date_created = (
            datetime.datetime.strptime(
                '2017-08-30T23:04:54.014Z',
                '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        )
        date_modified = (
            datetime.datetime.strptime(
                '2017-08-31T00:02:41.493Z',
                '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        )

        self.assertEqual(template_lookup.template_id, template_id)
        self.assertEqual(template_lookup.created, date_created)
        self.assertEqual(template_lookup.created, date_modified)
        self.assertEqual(template_lookup.last_used, 'UNKNOWN')
        self.assertEqual(template_lookup.name, 'Welcome Message')
        self.assertEqual(template_lookup.description, 'Our welcome message')
        self.assertEqual(
            template_lookup.variables,
            [
                {
                    'key': 'TITLE',
                    'name': 'Title',
                    'description': 'e.g. Mr, Ms, Dr, etc.',
                    'default_value': ''
                },
                {
                    'key': 'FIRST_NAME',
                    'name': 'First Name',
                    'description': 'Given name',
                    'default_value': None
                },
                {
                    'key': 'LAST_NAME',
                    'name': 'Last Name',
                    'description': 'Family name',
                    'default_value': None
                }
            ]
        )
        self.assertEqual(
            template_lookup.push,
            {
                'notification': {
                    'alert': 'Hello {{FIRST_NAME}}, this is your '
                             'welcome message!'
                }
            }
        )
