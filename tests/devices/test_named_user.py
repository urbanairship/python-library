import unittest
import json

import mock
from mock import Mock
import requests

import urbanairship as ua


class TestNamedUser(unittest.TestCase):
    def test_Named_User(self):
        name = 'named_user_id'

        ok_true = json.dumps({'ok': True}).encode('utf-8')

        associate_response = requests.Response()
        associate_response.status_code = 200
        associate_response._content = ok_true

        disassociate_response = requests.Response()
        disassociate_response._content = ok_true
        disassociate_response.status_code = 200

        lookup_response = requests.Response()
        lookup_response._content = json.dumps({
            'ok': True,
            'named_user': {
                'named_user_id': 'name1',
                'tags': {'group_name': ['tag1', 'tag2']}
            }
        }).encode('utf-8')

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [
            associate_response, disassociate_response, lookup_response
        ]

        airship = ua.Airship('key', 'secret')

        nu = ua.NamedUser(airship, 'name1')

        associate = nu.associate('channel_id', 'ios')

        self.assertEqual(associate.status_code, 200)
        self.assertEqual(associate.ok, True)

        disassociate = nu.disassociate('channel_id', 'ios')
        self.assertEqual(disassociate.status_code, 200)
        self.assertEqual(disassociate.ok, True)

        lookup = nu.lookup()

        self.assertEqual(lookup['ok'], True)
        self.assertEqual(lookup['named_user'], {
            'named_user_id': 'name1',
            'tags': {'group_name': ['tag1', 'tag2']}
        })

    def test_named_user_tag(self):
        airship = ua.Airship('key', 'secret')
        nu = ua.NamedUser(airship, 'named_user_id')

        self.assertRaises(
            ValueError,
            nu.tag,
            add={'group': 'tag'},
            set={'group': 'other_tag'}
        )


class TestNamedUserList(unittest.TestCase):
    def test_NamedUserlist_iteration(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    'named_users': [
                        {'named_user_id': 'name1'},
                        {'named_user_id': 'name2'},
                        {'named_user_id': 'name3'}
                    ]
                }
            ).encode('utf-8')
            mock_request.return_value = response

            name_list = ['name3', 'name2', 'name1']
            airship = ua.Airship('key', 'secret')
            named_user_list = ua.NamedUserList(airship)

            for a in named_user_list:
                self.assertEqual(a.named_user_id, name_list.pop())
