import unittest
import mock
from mock import Mock
import requests
import urbanairship as ua
import json


class TestSegmentList(unittest.TestCase):
    def test_segment_list(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "segments": [
                        {"display_name": "test1"},
                        {"display_name": "test2"}
                    ]
                }
            ).encode('utf-8')
            mock_request.return_value = response

            name_list = ['test2', 'test1']
            airship = ua.Airship('key', 'secret')
            seg_list = ua.SegmentList(airship)

            for a in seg_list:
                self.assertEqual(a.display_name, name_list.pop())


class TestSegment(unittest.TestCase):
    def test_segment_create_update_delete(self):
        name = 'test_segment'
        criteria = json.dumps(
            {
                'and': [
                    {'tag': 'TEST'},
                    {'not': {'tag': 'TEST2'}}
                ]
            }
        )

        data = json.dumps({
            'name': name,
            'criteria': criteria
        }).encode('utf-8')

        create_response = requests.Response()
        create_response.status_code = 200
        create_response.headers['location'] = ('https://go.urbanairship.com/'
                                               'api/segments/1234')

        id_response = requests.Response()
        id_response._content = data
        id_response.status_code = 200


        update_response = requests.Response()
        update_response.status_code = 200

        del_response = requests.Response()
        del_response.status_code = 204

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [create_response, id_response,
                                           id_response, update_response,
                                           del_response]

        airship = ua.Airship('key', 'secret')

        seg = ua.Segment()
        seg.display_name = name
        seg.criteria = criteria
        create_res = seg.create(airship)

        self.assertEqual(create_res.status_code, 200)
        self.assertEqual(seg.display_name, name)
        self.assertEqual(seg.criteria, criteria)

        from_id = seg.from_id(airship, 'test_id')
        self.assertEqual(from_id.name, name)
        self.assertEqual(from_id.criteria, criteria)

        seg.display_name = 'new_test_segment'
        up_res = seg.update(airship)
        del_res = seg.delete(airship)

        self.assertEqual(up_res.status_code, 200)
        self.assertEqual(del_res.status_code, 204)