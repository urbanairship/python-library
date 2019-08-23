import unittest
import mock
import json

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.operation_id = 'd67d4de6-934f-4ebb-aef0-250d89699b6b'
        self.experiment_id = 'f0c975e4-c01a-436b-92a0-2a360f87b211'
        self.push_id = '0edb9e6f-2198-4c42-aada-5a49eb03bcbb'
        self.audience = 'all'
        self.device_types = 'android'
        self.variants = []

        #create a push object (better 2 so it's unic / variant)

    def test_simple_experiment(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dump({
                "ok": True,
                "operation_id": self.operation_id,
                "experiment_id": self.experiment_id,
                "push_id": self.push_id
            }).encode('utf-8')
            response.status_code = 201
            mock_request.return_value = response

            experiment_object = ua.Experiment(airship=self.airship,
                                              audiance=self.audience,
                                              device_types=self.device_types,
                                              variants=self.variants)

            r = experiment_object.register()

            self.assertEqual(self.operation_id, experiment_object.operation_id)
            self.assertEqual(self.experiment_id, experiment_object.experiment_id)
            self.assertEqual(self.push_id, experiment_object.push_id)
            self.assertEqual(201, r.status_code)
