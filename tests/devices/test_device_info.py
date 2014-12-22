import json
import unittest
import mock
import requests
import datetime
import urbanairship as ua

class TestDeviceInfo(unittest.TestCase):

    def test_channel_list(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = ('''{"channels":[
                                 {"channel_id": "0492662a-1b52-4343-a1f9-c6b0c72931c0"},
                                 {"channel_id": "d95ceae2-85cb-41b7-a87d-09c9b3ce4051"},
                                 {"channel_id": "f10cf38c-3fbd-47e8-a4aa-43cf91d80ba1"}]}''')
            response.status_code = 200
            mock_request.return_value = response

            url = "https://go.urbanairship.com/api/channels/0492662a-1b52-4343-a1f9-c6b0c72931c0"

            airship = ua.Airship("key", "secret")
            channel_list = ua.ChannelList(airship, url)
            channel1 = channel_list.next()
            channel2 = channel_list.next()
            channel3 = channel_list.next()

            self.assertEqual(channel1.channel_id, "0492662a-1b52-4343-a1f9-c6b0c72931c0")
            self.assertEqual(channel2.channel_id, "d95ceae2-85cb-41b7-a87d-09c9b3ce4051")
            self.assertEqual(channel3.channel_id, "f10cf38c-3fbd-47e8-a4aa-43cf91d80ba1")


    def test_channel_lookup(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = json.dumps(
                {
                    "channel":{
                        "channel_id":"0492662a-1b52-4343-a1f9-c6b0c72931c0",
                        "device_type":"ios",
                        "installed":"false",
                        "opt_in":"false",
                        "background":"false",
                        "push_address":"3C0590EBCC11618723B3D4C8AA60BCFB6",
                        "created":"2014-04-17T23:35:15",
                        "last_registration":"2014-08-11T20:47:28",
                        "alias":"null",
                        "tags":["test_tag"],
                        "ios":{
                            "badge":1,
                            "quiettime":{
                                "start":"null",
                                "end":"null"
                            },
                            "tz":"null",
                        }
                    }
                }
            )

            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship("key", "secret")
            channel_id = "0492662a-1b52-4343-a1f9-c6b0c72931c0"
            channel_lookup = ua.ChannelInfo.lookup(airship, channel_id)

            self.assertEqual(channel_lookup.channel_id, channel_id)
            self.assertEqual(channel_lookup.device_type, "ios")
            self.assertEqual(channel_lookup.installed, "false")
            self.assertEqual(channel_lookup.opt_in, "false")
            self.assertEqual(channel_lookup.background, "false")
            self.assertEqual(channel_lookup.push_address, "3C0590EBCC11618723B3D4C8AA60BCFB6")
            self.assertEqual(channel_lookup.created, "2014-04-17T23:35:15")
            self.assertEqual(channel_lookup.last_registration, "2014-08-11T20:47:28")
            self.assertEqual(channel_lookup.alias, "null")
            self.assertEqual(channel_lookup.tags, ["test_tag"])
            self.assertEqual(channel_lookup.ios, {"badge":1,"quiettime":{"start":"null","end":"null"},"tz":"null"})

    def test_device_token_feedback(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = ('''[{
                                   "alias" : null,
                                   "device_token" : "4D95CB349F95ADEBE05F0A71B5F5B62D0F696667454DA60CD55282F67321710C",
                                   "marked_inactive_on" : "2014-12-16 20:21:42"
                                 }]''')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship("key", "secret")
            feedback = ua.Feedback.device_token(airship, datetime.datetime(2014,11,22))
            date = '2014-12-16 20:21:42'
            try:
                from dateutil.parser import parse
                date = parse(date)
            except ImportError:
                def parse(date):
                    return date

            self.assertEqual(feedback,[{u'device_token': u'4D95CB349F95ADEBE05F0A71B5F5B62D0F696667454DA60CD55282F67321710C',
                                        u'alias': None,
                                        u'marked_inactive_on': date}
                                       ])
            mock_request.assert_called_with('GET', '', 'https://go.urbanairship.com/api/device_tokens/feedback/',
                                            version=3, params={'since': '2014-11-22T00:00:00'}
                                            )

    def test_apid_feedback(self):
        with mock.patch.object(ua.Airship, "_request") as mock_request:
            response = requests.Response()
            response._content = ('''[{
                                   "alias" : null,
                                   "apid" : "80242a4c-d870-4fce-b0c3-724c865cfbfe",
                                   "gcm_registration_id": "null",
                                   "marked_inactive_on" : "2014-12-16 20:21:42"
                                 }]''')
            response.status_code = 200
            mock_request.return_value = response

            airship = ua.Airship("key", "secret")
            feedback = ua.Feedback.apid(airship, datetime.datetime(2014, 11, 22, 10, 10, 10))
            date = '2014-12-16 20:21:42'
            try:
                from dateutil.parser import parse
                date = parse(date)
            except ImportError:
                def parse(date):
                    return date

            self.assertEqual(feedback,[{u'apid': u'80242a4c-d870-4fce-b0c3-724c865cfbfe',
                                        u'alias': None,
                                        u'marked_inactive_on': date,
                                        u'gcm_registration_id': u'null'}
                                       ])
            mock_request.assert_called_with('GET', '', 'https://go.urbanairship.com/api/apids/feedback/',
                                            version=3, params={'since': '2014-11-22T10:10:10'}
                                            )
