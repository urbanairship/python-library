import datetime
import json
import unittest

import mock
import requests

import urbanairship as ua
from tests import TEST_KEY, TEST_SECRET


class TestDeviceInfo(unittest.TestCase):
    def test_channel_list(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channels": [
                        {"channel_id": "0492662a-1b52-4343-a1f9-c6b0c72931c0"},
                        {"channel_id": "d95ceae2-85cb-41b7-a87d-09c9b3ce4051"},
                        {"channel_id": "f10cf38c-3fbd-47e8-a4aa-43cf91d80ba1"},
                    ]
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            url = "https://go.urbanairship.com/api/channels/0492662a-1b52-4343-a1f9-c6b0c72931c0"

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_list = ua.ChannelList(airship, url)
            channel_id_list = []

            for channel in channel_list:
                channel_id_list.append(channel.channel_id)

            self.assertEqual(channel_id_list[0], "0492662a-1b52-4343-a1f9-c6b0c72931c0")
            self.assertEqual(channel_id_list[1], "d95ceae2-85cb-41b7-a87d-09c9b3ce4051")
            self.assertEqual(channel_id_list[2], "f10cf38c-3fbd-47e8-a4aa-43cf91d80ba1")

    def test_channel_lookup(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel": {
                        "channel_id": "0492662a-1b52-4343-a1f9-c6b0c72931c0",
                        "device_type": "ios",
                        "installed": "false",
                        "opt_in": "false",
                        "background": "false",
                        "push_address": "3C0590EBCC11618723B3D4C8AA60BCFB6",
                        "created": "2014-04-17T23:35:15",
                        "last_registration": "None",
                        "alias": "null",
                        "tags": ["test_tag"],
                        "ios": {
                            "badge": 1,
                            "quiettime": {"start": "null", "end": "null"},
                            "tz": "null",
                        },
                    }
                }
            ).encode("utf-8")

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_id = "0492662a-1b52-4343-a1f9-c6b0c72931c0"
            channel_lookup = ua.ChannelInfo(airship).lookup(channel_id)

            date_created = datetime.datetime.strptime("2014-04-17T23:35:15", "%Y-%m-%dT%H:%M:%S")

            self.assertEqual(channel_lookup.channel_id, channel_id)
            self.assertEqual(channel_lookup.device_type, "ios")
            self.assertEqual(channel_lookup.installed, "false")
            self.assertEqual(channel_lookup.opt_in, "false")
            self.assertEqual(channel_lookup.background, "false")
            self.assertEqual(channel_lookup.alias, "null")
            self.assertEqual(channel_lookup.tags, ["test_tag"])
            self.assertEqual(channel_lookup.created, date_created)
            self.assertEqual(channel_lookup.push_address, "3C0590EBCC11618723B3D4C8AA60BCFB6")
            self.assertEqual(channel_lookup.last_registration, "UNKNOWN")
            self.assertEqual(
                channel_lookup.ios,
                {
                    "badge": 1,
                    "quiettime": {"start": "null", "end": "null"},
                    "tz": "null",
                },
            )

    def test_channel_info_datetime_parsing_with_none_values(self):
        """Test that ChannelInfo handles None values for datetime fields correctly."""
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel": {
                        "channel_id": "test-channel-id",
                        "device_type": "ios",
                        "created": "2023-01-01T12:00:00",
                        "last_registration": None,  # This should not cause a ValueError
                        "commercial_opted_in": None,
                        "commercial_opted_out": None,
                        "transactional_opted_in": None,
                        "transactional_opted_out": None,
                    }
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_info = ua.ChannelInfo(airship).lookup("test-channel-id")

            # Valid datetime should be parsed
            expected_created = datetime.datetime.strptime(
                "2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"
            )
            self.assertEqual(channel_info.created, expected_created)

            # None values should remain None (not converted to "UNKNOWN")
            self.assertIsNone(channel_info.last_registration)
            self.assertIsNone(channel_info.commercial_opted_in)
            self.assertIsNone(channel_info.commercial_opted_out)
            self.assertIsNone(channel_info.transactional_opted_in)
            self.assertIsNone(channel_info.transactional_opted_out)

    def test_channel_info_datetime_parsing_with_empty_strings(self):
        """Test that ChannelInfo handles empty strings for datetime fields correctly."""
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel": {
                        "channel_id": "test-channel-id",
                        "device_type": "ios",
                        "created": "2023-01-01T12:00:00",
                        "last_registration": "",  # Empty string should not cause ValueError
                        "commercial_opted_in": "",
                    }
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_info = ua.ChannelInfo(airship).lookup("test-channel-id")

            # Valid datetime should be parsed
            expected_created = datetime.datetime.strptime(
                "2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"
            )
            self.assertEqual(channel_info.created, expected_created)

            # Empty strings should remain empty strings
            self.assertEqual(channel_info.last_registration, "")
            self.assertEqual(channel_info.commercial_opted_in, "")

    def test_channel_info_datetime_parsing_with_invalid_strings(self):
        """Test that ChannelInfo handles invalid datetime strings correctly."""
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel": {
                        "channel_id": "test-channel-id",
                        "device_type": "ios",
                        "created": "2023-01-01T12:00:00",
                        "last_registration": "invalid-datetime",  # Should become "UNKNOWN"
                        "commercial_opted_in": "not-a-date",
                    }
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_info = ua.ChannelInfo(airship).lookup("test-channel-id")

            # Valid datetime should be parsed
            expected_created = datetime.datetime.strptime(
                "2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"
            )
            self.assertEqual(channel_info.created, expected_created)

            # Invalid datetime strings should become "UNKNOWN"
            self.assertEqual(channel_info.last_registration, "UNKNOWN")
            self.assertEqual(channel_info.commercial_opted_in, "UNKNOWN")

    def test_device_info_datetime_parsing_with_none_values(self):
        """Test that DeviceInfo handles None values for datetime fields correctly."""
        # Test DeviceInfo.from_payload directly
        airship = ua.Airship(TEST_KEY, TEST_SECRET)

        # Test with None value for created field
        payload = {
            "device_token": "test-device-token",
            "created": None,  # This should not cause a ValueError
            "active": True,
            "tags": ["test_tag"],
        }

        device_info = ua.DeviceInfo.from_payload(payload, "device_token", airship)

        # None value should remain None
        self.assertIsNone(device_info.created)
        self.assertEqual(device_info.id, "test-device-token")
        self.assertEqual(device_info.device_type, "device_token")
        self.assertTrue(device_info.active)
        self.assertEqual(device_info.tags, ["test_tag"])

    def test_device_info_datetime_parsing_with_valid_datetime(self):
        """Test that DeviceInfo correctly parses valid datetime strings."""
        airship = ua.Airship(TEST_KEY, TEST_SECRET)

        payload = {
            "device_token": "test-device-token",
            "created": "2023-01-01 12:00:00",  # Space-separated format for DeviceInfo
            "active": True,
            "tags": ["test_tag"],
        }

        device_info = ua.DeviceInfo.from_payload(payload, "device_token", airship)

        # Valid datetime should be parsed
        expected_created = datetime.datetime.strptime("2023-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        self.assertEqual(device_info.created, expected_created)

    def test_device_info_datetime_parsing_with_invalid_strings(self):
        """Test that DeviceInfo handles invalid datetime strings correctly."""
        airship = ua.Airship(TEST_KEY, TEST_SECRET)

        payload = {
            "device_token": "test-device-token",
            "created": "invalid-datetime",  # Should become "UNKNOWN"
            "active": True,
            "tags": ["test_tag"],
        }

        device_info = ua.DeviceInfo.from_payload(payload, "device_token", airship)

        # Invalid datetime string should become "UNKNOWN"
        self.assertEqual(device_info.created, "UNKNOWN")

    def test_channel_info_opt_in_date_opt_out_date_with_none_values(self):
        """Test that ChannelInfo handles None values for opt_in_date and opt_out_date correctly."""
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel": {
                        "channel_id": "test-channel-id",
                        "device_type": "ios",
                        "created": "2023-01-01T12:00:00",
                        "opt_in_date": None,  # This should not cause a ValueError
                        "opt_out_date": None,  # This should not cause a ValueError
                    }
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_info = ua.ChannelInfo(airship).lookup("test-channel-id")

            # Valid datetime should be parsed
            expected_created = datetime.datetime.strptime(
                "2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"
            )
            self.assertEqual(channel_info.created, expected_created)

            # None values should remain None (not converted to "UNKNOWN")
            self.assertIsNone(channel_info.opt_in_date)
            self.assertIsNone(channel_info.opt_out_date)

    def test_channel_info_opt_in_date_opt_out_date_with_valid_datetime(self):
        """Test that ChannelInfo correctly parses valid opt_in_date and opt_out_date datetime strings."""
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel": {
                        "channel_id": "test-channel-id",
                        "device_type": "ios",
                        "created": "2023-01-01T12:00:00",
                        "opt_in_date": "2023-01-15T10:30:00",
                        "opt_out_date": "2023-02-20T14:45:00",
                    }
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_info = ua.ChannelInfo(airship).lookup("test-channel-id")

            # Valid datetime should be parsed
            expected_created = datetime.datetime.strptime(
                "2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"
            )
            expected_opt_in_date = datetime.datetime.strptime(
                "2023-01-15T10:30:00", "%Y-%m-%dT%H:%M:%S"
            )
            expected_opt_out_date = datetime.datetime.strptime(
                "2023-02-20T14:45:00", "%Y-%m-%dT%H:%M:%S"
            )
            self.assertEqual(channel_info.created, expected_created)
            self.assertEqual(channel_info.opt_in_date, expected_opt_in_date)
            self.assertEqual(channel_info.opt_out_date, expected_opt_out_date)

    def test_channel_info_opt_in_date_opt_out_date_with_empty_strings(self):
        """Test that ChannelInfo handles empty strings for opt_in_date and opt_out_date correctly."""
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel": {
                        "channel_id": "test-channel-id",
                        "device_type": "ios",
                        "created": "2023-01-01T12:00:00",
                        "opt_in_date": "",  # Empty string should not cause ValueError
                        "opt_out_date": "",  # Empty string should not cause ValueError
                    }
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_info = ua.ChannelInfo(airship).lookup("test-channel-id")

            # Valid datetime should be parsed
            expected_created = datetime.datetime.strptime(
                "2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"
            )
            self.assertEqual(channel_info.created, expected_created)

            # Empty strings should remain empty strings
            self.assertEqual(channel_info.opt_in_date, "")
            self.assertEqual(channel_info.opt_out_date, "")

    def test_channel_info_opt_in_date_opt_out_date_with_invalid_strings(self):
        """Test that ChannelInfo handles invalid opt_in_date and opt_out_date datetime strings correctly."""
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel": {
                        "channel_id": "test-channel-id",
                        "device_type": "ios",
                        "created": "2023-01-01T12:00:00",
                        "opt_in_date": "invalid-datetime",  # Should become "UNKNOWN"
                        "opt_out_date": "not-a-date",  # Should become "UNKNOWN"
                    }
                }
            ).encode("utf-8")
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship(TEST_KEY, TEST_SECRET)
            channel_info = ua.ChannelInfo(airship).lookup("test-channel-id")

            # Valid datetime should be parsed
            expected_created = datetime.datetime.strptime(
                "2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"
            )
            self.assertEqual(channel_info.created, expected_created)

            # Invalid datetime strings should become "UNKNOWN"
            self.assertEqual(channel_info.opt_in_date, "UNKNOWN")
            self.assertEqual(channel_info.opt_out_date, "UNKNOWN")
