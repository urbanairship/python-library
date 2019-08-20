import datetime
import json
import mock
import requests
import unittest

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


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
    def test_template_lookup1(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'ok': True,
                    'template': {
                        'id': 'ef34a8d9-0ad7-491c-86b0-aea74da15161',
                        'created_at': '2017-08-30T23:04:54.014Z',
                        'modified_at': None,
                        'last_used': None,
                        'name': 'Welcome Message',
                        'description': '',
                        'variables': [
                            {
                                'key': 'FIRST_NAME',
                                'name': 'First Name',
                                'description': 'Given name',
                                'default_value': None
                            }
                        ],
                        'push': {
                            'notification': {
                                'alert': 'Hello {{FIRST_NAME}}, this is your '
                                         'welcome message!'
                            }
                        }
                    }
                }
            ).encode('utf-8')
        
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'

        self.assertEqual(airship.urls.get('templates_url') + template_id,
                        'https://go.urbanairship.com/api/templates/' + template_id)


    def test_template_lookup2(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'ok': True,
                    'template': {
                        'id': 'ef34a8d9-0ad7-491c-86b0-aea74da15161',
                        'created_at': '2017-08-30T23:04:54.014Z',
                        'modified_at': '2017-08-31T00:02:41.493Z',
                        'last_used': None,
                        'name': 'Welcome Message',
                        'description': 'A welcome message',
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
                                'alert': 'Hello {{FIRST_NAME}}, this is your '
                                         'welcome message!'
                            }
                        }
                    }
                }
            ).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'
            template_lookup = ua.Template(airship).lookup(template_id)

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
            self.assertEqual(template_lookup.created_at, date_created)
            self.assertEqual(template_lookup.modified_at, date_modified)
            self.assertEqual(template_lookup.last_used, 'UNKNOWN')
            self.assertEqual(template_lookup.name, 'Welcome Message')
            self.assertEqual(template_lookup.description, 'A welcome message')
            self.assertListEqual(
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
            self.assertDictEqual(
                template_lookup.push,
                {
                    'notification': {
                        'alert': 'Hello {{FIRST_NAME}}, this is your '
                                 'welcome message!'
                    }
                }
            )

    def test_template_listing(self):
        self.template1 = 'b8f9b663-0a3b-cf45-587a-be880946e881'
        self.template2 = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'ok': True,
                    'total_count': 2,
                    'templates': [
                        {
                            'id': 'b8f9b663-0a3b-cf45-587a-be880946e881',
                            'name': 'Template test',
                            'description': 'A template description',
                            'variables': [
                                {
                                    'key': 'FIRST_NAME',
                                    'name': 'First Name',
                                    'description': 'Given name',
                                    'default_value': None
                                }
                            ],
                            'created_at': '2017-08-30T23:04:54.014Z',
                            'modified_at': '2017-08-31T00:02:41.493Z',
                            'push': {
                                'notification': {
                                    'alert': 'Hello {{FIRST_NAME}}, this is '
                                             'a test'
                                }
                            },
                            'last_used': None
                        },
                        {
                            'id': 'ef34a8d9-0ad7-491c-86b0-aea74da15161',
                            'name': 'Welcome Message',
                            'description': 'A welcome message',
                            'variables': [
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
                                    'default_value': 'Smith'
                                },
                                {
                                    'key': 'TITLE',
                                    'name': 'Title',
                                    'description': 'e.g. Mr, Ms, Dr, etc.',
                                    'default_value': ''
                                }
                            ],
                            'created_at': '2017-08-31T20:18:10.924Z',
                            'modified_at': '2017-08-31T20:18:10.924Z',
                            'push': {
                                'notification': {
                                    'alert': 'Hello {{TITLE}} {{FIRST_NAME}} '
                                             '{{LAST_NAME}}!'
                                }
                            },
                            'last_used': '2017-08-31T21:00:00.00Z'
                        }
                    ],
                    'count': 2,
                    'next_page': None,
                    'prev_page': None
                }
            ).encode('utf-8')

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)

            template_responses = []

            for template in ua.TemplateList(airship):
                template_responses.append(template)

            self.assertEquals(
                template_responses[0].template_id, self.template1
            )
            self.assertEquals(
                template_responses[1].template_id, self.template2
            )

            self.assertEquals(
                template_responses[0].created_at,
                datetime.datetime.strptime(
                    '2017-08-30T23:04:54.014Z',
                    '%Y-%m-%dT%H:%M:%S.%fZ'
                )
            )
            self.assertEquals(
                template_responses[1].modified_at,
                datetime.datetime.strptime(
                    '2017-08-31T20:18:10.924Z',
                    '%Y-%m-%dT%H:%M:%S.%fZ'
                )
            )
            self.assertEquals(template_responses[0].last_used, 'UNKNOWN')

    def test_template_creation_payload(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        t = ua.Template(airship)
        t.name = 'Welcome Message'
        t.description = 'A welcome message'
        t.variables = [
            {
                'key': 'TITLE',
                'name': 'Title',
                'description': 'e.g. Mr., Ms., Dr., etc.',
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
                'default_value': 'Smith'
            }
        ]
        t.push = {
            'notification': {
                'alert': 'Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}!'
            }
        }

        self.assertDictEqual(
            t.payload,
            {
                'push': {
                    'notification': {
                        'alert': 'Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}!'
                    }
                },
                'variables': [
                    {
                        'default_value': '',
                        'name': 'Title',
                        'key': 'TITLE',
                        'description': 'e.g. Mr., Ms., Dr., etc.'
                    },
                    {
                        'default_value': None,
                        'name': 'First Name',
                        'key': 'FIRST_NAME',
                        'description': 'Given name'
                    },
                    {
                        'default_value': 'Smith',
                        'name': 'Last Name',
                        'key': 'LAST_NAME',
                        'description': 'Family name'
                    }
                ],
                'name': 'Welcome Message',
                'description': 'A welcome message'
            }
        )

    def test_create_template(self):
        template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'
        name = 'Welcome Message'
        description = 'A welcome message'
        variables = [
            {
                'key': 'TITLE',
                'name': 'Title',
                'description': 'e.g. Mr., Ms., Dr., etc.',
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
                'default_value': 'Smith'
            }
        ]
        push = {
            'notification': {
                'alert': 'Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}!'
            }
        }

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'ok': True,
                    'operation_id': '9ce808c8-7176-45dc-b79e-44aa74249a5a',
                    'template_id': 'ef34a8d9-0ad7-491c-86b0-aea74da15161'
                }
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            template = ua.Template(airship)
            template.name = name
            template.description = description
            template.variables = variables
            template.push = push

            template.create()

            self.assertEqual(template.template_id, template_id)

    def test_create_template_requires_name(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        template = ua.Template(airship)
        # Do not set name
        template.description = 'The cat says...'
        template.variables = [{
                'key': 'SOUND',
                'name': 'Sound',
                'description': 'A sound',
                'default_value': 'Meow'
            }
        ]
        template.push = {'notification': {'alert': 'The cat says {{SOUND}}'}}

        self.assertRaises(ValueError, template.create)

    def test_create_template_requires_push(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        template = ua.Template(airship)
        # Do not set push
        template.name = 'Cat sound'
        template.description = 'The cat says...'
        template.variables = [{
                'key': 'SOUND',
                'name': 'Sound',
                'description': 'A sound',
                'default_value': 'Meow'
            }
        ]

        self.assertRaises(ValueError, template.create)

    def test_create_template_no_message(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        template = ua.Template(airship)
        template.name = 'Cat sound'
        template.description = 'The cat says...'
        template.variables = [{
                'key': 'SOUND',
                'name': 'Sound',
                'description': 'A sound',
                'default_value': 'Meow'
            }
        ]
        # Set message center (not allowed)
        template.push = {
            'notification': {'alert': 'The cat says {{SOUND}}'},
            'message': {
                'title': 'Message title',
                'body': 'Message body',
                'content_type': 'text/html'
            }
        }

        self.assertRaises(ValueError, template.create)

    def test_update_template(self):
        template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'
        name = 'Goodbye Message'
        description = 'A goodbye message'
        push = {
            'notification': {
                'alert': 'Bye {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}}!'
            }
        }

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'ok': True,
                    'operation_id': '9ce808c8-7176-45dc-b79e-44aa74249a5a'
                }
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            template = ua.Template(airship)
            template.name = name
            template.description = description
            template.push = push

            template.update(template_id)

            self.assertEqual(template.template_id, template_id)

    def test_update_template_no_message(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'
        template = ua.Template(airship)
        # Set message center (not allowed)
        template.push = {
            'notification': {'alert': 'The cat says {{SOUND}}'},
            'message': {
                'title': 'Message title',
                'body': 'Message body',
                'content_type': 'text/html'
            }
        }

        self.assertRaises(ValueError, template.update, template_id)

    def test_update_template_needs_something(self):
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'
        template = ua.Template(airship)
        # Don't set anything

        self.assertRaises(ValueError, template.update, template_id)

    def test_delete_template(self):
        template_id = 'ef34a8d9-0ad7-491c-86b0-aea74da15161'

        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'ok': True,
                    'operation_id': 'a6394ff8-8a65-4494-ad06-677eb8b7ad6a'
                }
            ).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            template = ua.Template(airship)
            template.delete(template_id)

            self.assertEqual(template.template_id, template_id)
