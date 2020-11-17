import json
import unittest
import mock
import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestLocationFinder(unittest.TestCase):
    def setUp(self):
        self.lat1 = 37.63983
        self.long1 = -123.173825
        self.lat2 = 37.929824
        self.long2 = -122.28178
        mock_response = requests.Response()
        mock_response._content = json.dumps({
            "features": [{
                "bounds": [
                    self.lat1,
                    self.long1,
                    self.lat2,
                    self.long2
                ],
                "centroid": [
                    37.759715,
                    -122.693976
                ],
                "id": "4oFkxX7RcUdirjtaenEQIV",
                "properties": {
                    "boundary_type": "city",
                    "boundary_type_string": "City/Place",
                    "context": {
                        "us_state": "CA",
                        "us_state_name": "California"
                    },
                    "name": "San Francisco",
                    "source": "tiger.census.gov"
                },
                "type": "Feature"
            }]
        }).encode('utf-8')
        ua.Airship._request = mock.Mock()
        ua.Airship._request.side_effect = [mock_response]
        airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.loc_finder = ua.LocationFinder(airship)

    def test_name_lookup(self):
        info = self.loc_finder.name_lookup('name')
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_name_lookup_with_type(self):
        info = self.loc_finder.name_lookup('name', 'type')
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_coordinates_lookup(self):
        info = self.loc_finder.coordinates_lookup(123, 123)
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_coordinates_lookup_with_type(self):
        info = self.loc_finder.coordinates_lookup(123, 123, 'type')
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_invalid_coordinates(self):
        self.assertRaises(
            TypeError,
            self.loc_finder,
            latitude='123',
            longitude=123
        )

    def test_bounding_box_lookup(self):
        info = self.loc_finder.bounding_box_lookup(123, 123, 123, 123)
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_bounding_box_lookup_with_type(self):
        info = self.loc_finder.bounding_box_lookup(123, 123, 123, 123, 'type')
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_invalid_bounding_box(self):
        self.assertRaises(
            TypeError,
            self.loc_finder.bounding_box_lookup,
            lat1='123',
            long1=123,
            lat2=123,
            long2=123
        )

    def test_alias_lookup(self):
        info = self.loc_finder.alias_lookup('alias=alias')
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_alias_list_lookup(self):
        info = self.loc_finder.alias_lookup(['alias=alias1', 'alias=alias2'])
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_polygon_lookup(self):
        info = self.loc_finder.polygon_lookup('id', 1)
        self.assertEqual(
            info['features'][0]['bounds'],
            [self.lat1, self.long1, self.lat2, self.long2]
        )

    def test_invalid_zoom(self):
        self.assertRaises(
            TypeError,
            self.loc_finder.polygon_lookup,
            polygon_id='id',
            zoom='1'
        )

    def test_date_ranges(self):
        expected_resp = [
            {'unit': 'hours', 'cutoff': '2015-10-01 15'},
            {'unit': 'days', 'cutoff': '2015-10-01'},
            {'unit': 'weeks', 'cutoff': '2015-W10'},
            {'unit': 'months', 'cutoff': '2015-10'},
            {'unit': 'years', 'cutoff': '2015-10'}
        ]
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            mock_response = requests.Response()
            mock_response._content = json.dumps(expected_resp).encode('utf-8')
            mock_request.return_value = mock_response
            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            location = ua.LocationFinder(airship)
            actual_resp = location.date_ranges()
            self.assertEqual(actual_resp, expected_resp)
