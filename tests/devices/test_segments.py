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
            response._content = (
                '''
                 {"segments":[
                      {"display_name":"test1"},
                      {"display_name":"test2"}]}
                ''')

            mock_request.return_value = response
            airship = ua.Airship('key', 'secret')
            seg_list = ua.SegmentList(airship)

            name_list = ['test2', 'test1']

            for a in seg_list:
                self.assertEqual(a.display_name, name_list.pop())


class TestSegment(unittest.TestCase):
    def test_segment_create_update_delete(self):
        seg_class = ua.Segment()
        airship = ua.Airship('key', 'secret')
        name = "test_segment"
        criteria = json.dumps(
            {'and': [{'tag': 'TEST'}, {'not': {'tag': 'TEST2'}}]}
        ).encode('utf-8')

        create_response = requests.Response()
        create_response._content = json.dumps(
            {'display_name': name, 'criteria': criteria}).encode('utf-8')
        create_response.status_code = 200

        id_response = requests.Response()
        id_response._content = name
        id_response.status_code = 200
        id_response.headers[
            'location'] = "https://go.urbanairship.com/api/segments/1234"

        update_response = requests.Response()
        update_response.status_code = 200

        del_response = requests.Response()
        del_response.status_code = 204

        ua.Airship._request = Mock()
        ua.Airship._request.side_effect = [id_response, create_response,
                                           update_response, del_response]

        segment = seg_class.create(airship, name, criteria)
        self.assertEqual(segment.display_name, name)
        self.assertEqual(segment.criteria, criteria)

        segment.display_name = 'new_test_segment'
        upres = segment.update()

        self.assertEqual(upres.status_code, 200)

        delres = segment.delete()

        self.assertEqual(delres.status_code, 204)