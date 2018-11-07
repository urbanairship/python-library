import json
import mock
import unittest
import uuid

import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestEmail(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.address = 'test_email@testing.xzy'
        self.locale_country = 'US'
        self.locale_language = 'en'
        self.timezone = 'America/Los_Angeles'
        self.channel_id = str(uuid.uuid4())

    def test_email_reg(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
                'channel_id': self.channel_id
            }).encode('utf-8')
            response.status_code = 201
            mock_request.return_value = response

            email_obj = ua.Email(airship=self.airship,
                                 address=self.address)

            r = email_obj.register()

            self.assertEqual(self.channel_id, email_obj.channel_id)
            self.assertEqual(201, r.status_code)

    def test_email_w_opt_dates(self):
        test_date = '2018-11-06T12:00:00Z'
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
                'channel_id': self.channel_id
            }).encode('utf-8')
            response.status_code = 201
            mock_request.return_value = response

            email_obj = ua.Email(airship=self.airship,
                                 address=self.address,
                                 commercial_opted_in=test_date,
                                 commercial_opted_out=test_date,
                                 transactional_opted_in=test_date,
                                 transactional_opted_out=test_date)

            r = email_obj.register()

            self.assertEqual(self.channel_id, email_obj.channel_id)
            self.assertEqual(201, r.status_code)

    def test_email_update(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
                'channel_id': self.channel_id
            }).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            email_obj = ua.Email(airship=self.airship,
                                 address=self.address)

            r = email_obj.register()

            self.assertEqual(self.channel_id, email_obj.channel_id)
            self.assertEqual(200, r.status_code)

    def test_email_reg_w_opts(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
                'channel_id': self.channel_id
            }).encode('utf-8')
            response.status_code = 201
            mock_request.return_value = response

            email_obj = ua.Email(airship=self.airship,
                                 address=self.address,
                                 locale_country=self.locale_country,
                                 locale_language=self.locale_language,
                                 timezone=self.timezone)

            r = email_obj.register()

            self.assertEqual(self.channel_id, email_obj.channel_id)
            self.assertEqual(201, r.status_code)

    def test_email_uninstall(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True,
                'channel_id': self.channel_id
            }).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            email_obj = ua.Email(airship=self.airship,
                                 address=self.address)

            r = email_obj.register()

            self.assertEqual(self.channel_id, email_obj.channel_id)
            self.assertEqual(200, r.status_code)


class TestEmailTags(unittest.TestCase):
    def setUp(self):
        self.airship = ua.Airship(TEST_KEY, TEST_SECRET)
        self.address = 'someone@xyz.fx'
        self.test_tags = ['one', 'two', 'three']
        self.test_group = 'test_group'

    def testTagAdd(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True
            })
            response.status_code = 200
            mock_request.return_value = response

            email_tags = ua.EmailTags(airship=self.airship,
                                      address=self.address)
            email_tags.add(group=self.test_group, tags=self.test_tags)
            response = email_tags.send()

            self.assertEqual(200, response.status_code)

    def testTagRemove(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True
            })
            response.status_code = 200
            mock_request.return_value = response

            email_tags = ua.EmailTags(airship=self.airship,
                                      address=self.address)
            email_tags.remove(group=self.test_group, tags=self.test_tags)
            response = email_tags.send()

            self.assertEqual(200, response.status_code)

    def testTagSet(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True
            })
            response.status_code = 200
            mock_request.return_value = response

            email_tags = ua.EmailTags(airship=self.airship,
                                      address=self.address)
            email_tags.remove(group=self.test_group, tags=self.test_tags)
            response = email_tags.send()

            self.assertEqual(200, response.status_code)

    def testSetWithAddAndRemove(self):
        with mock.patch.object(ua.Airship, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps({
                'ok': True
            })
            response.status_code = 200
            mock_request.return_value = response

            email_tags = ua.EmailTags(airship=self.airship,
                                      address=self.address)
            email_tags.set(group=self.test_group, tags=self.test_tags)
            email_tags.remove(group=self.test_group, tags=self.test_tags)

            with self.assertRaises(ValueError):
                email_tags.send()
