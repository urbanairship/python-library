import unittest

import urbanairship as ua


class TestTags(unittest.TestCase):

    def test__tag_list(self):
        my_app_tag_list = TagList(airship)
self.assertEqual(tags, {
            "tags": [
               "some_tag", 
               "portland_or",
               "another_tag"
            ]
      })

def test_add_device(self):
    with mock.patch.object(ua.Airship, '_request') as mock_request:
        response = requests.Response()
        response._content = (
            '''{"ios_channels": ["0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')
        response.status_code = 202
        mock_request.return_value = response

        airship = ua.Airship('key', 'secret')
        tag = tag.add()
        tag.payload = {}     # pick up here on Friday!
        pr = tag.apply()
        self.assertEqual(
            pr.tags, 'OK')

#     def test_add_device(self):              
#         tag = Tag(Airship, "high roller")
#         tag.add(ios_channels=['9c36e8c7-5a73-47c0-9716-99fd3d4197d5'])
#         tag.remove(android_channels=['channel_to_remove'])
#         self.assertEqual(ios_channels=['9c36e8c7-5a73-47c0-9716-99fd3d4197d5'], {  #?
#             "ios_channels": {
#                 "add": [
#                     "9c36e8c7-5a73-47c0-9716-99fd3d4197d5",
#                     "9c36e8c7-5a73-47c0-9716-99fd3d4197d6"
#                     ]
#             },
#             "android_channels": {
#                 "remove": [
#                     "channel_to_remove"
#                 ]
#             } 
#         })

#     def test_delete_tag(self):

#     def test_batch_tag(self):

# push = airship.create_push()
#    push.audience = ua.and_(
#       ua.tag("breakingnews"),
#       ua.or_(
#          ua.tag("sports"),
#          ua.tag("worldnews")
#       )
#    )
#    push.notification = ua.notification(
#       ios=ua.ios(
#          alert="Kim Jong-Un wins U.S. Open",
#          badge="+1",
#          extra={"articleid": "123456"}
#       ),
#       android=ua.android(
#          alert="Breaking Special Android News! Glorious Leader Kim Jong-Un wins U.S. Open!",
#          extra={"articleid": "http://m.example.com/123456"}
#       ),
#       amazon=ua.amazon(
#       alert='Breaking Amazon News!',
#       expires_after=60,
#       extra={'articleid': '12345'},
#       summary='This is a short message summary',
#       )
#    )
#    push.device_types = ua.device_types('ios', 'android', 'amazon')
#    push.send()