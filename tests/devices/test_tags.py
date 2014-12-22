import unittest

import urbanairship as ua


class TestTags(unittest.TestCase):

    def test__tag_listing(self):
            {
                "tags": []
            }
    def test_create_tag_success(self):
# def test_push_success(self):
#         with mock.patch.object(ua.Airship, '_request') as mock_request:
#             response = requests.Response()
#             response._content = (
#                 '''{"push_ids": ["0492662a-1b52-4343-a1f9-c6b0c72931c0"]}''')
#             response.status_code = 202
#             mock_request.return_value = response

#             airship = ua.Airship('key', 'secret')
#             push = airship.create_push()
#             push.audience = ua.all_
#             push.notification = ua.notification(alert='Hello')
#             push.options = ua.options(expiry=10080)
#             push.device_types = ua.all_
#             pr = push.send()
#             self.assertEqual(
#                 pr.push_ids, ['0492662a-1b52-4343-a1f9-c6b0c72931c0'])

    def test_add_tag_iOS(self):
    def test_add_tag_Android(self):
    def test_add_tag_Amazon(self):
    	# d = datetime.datetime(2015, 1, 1, 12, 56)
    	# self.assertEqual(ua.local_scheduled_time(d),
    	# 	{'local_scheduled_time': '2015-01-01T12:56:00'})

    def test_remove_tag_iOS(self):
    def test_remove_tag_Android(self):
    def test_remove_tag_Amazon(self):

    def test_batch_tag_iOS(self):
    def test_batch_tag_Android(self):
    def test_batch_tag_Amazon(self):

push = airship.create_push()
   push.audience = ua.and_(
      ua.tag("breakingnews"),
      ua.or_(
         ua.tag("sports"),
         ua.tag("worldnews")
      )
   )
   push.notification = ua.notification(
      ios=ua.ios(
         alert="Kim Jong-Un wins U.S. Open",
         badge="+1",
         extra={"articleid": "123456"}
      ),
      android=ua.android(
         alert="Breaking Special Android News! Glorious Leader Kim Jong-Un wins U.S. Open!",
         extra={"articleid": "http://m.example.com/123456"}
      ),
      amazon=ua.amazon(
      alert='Breaking Amazon News!',
      expires_after=60,
      extra={'articleid': '12345'},
      summary='This is a short message summary',
      )
   )
   push.device_types = ua.device_types('ios', 'android', 'amazon')
   push.send()