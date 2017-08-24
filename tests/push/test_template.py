import unittest

import urbanairship as ua


class TestTemplatePush(unittest.TestCase):
    def test_full_payload(self):
        p = ua.TemplatePush(None)
        p.audience = ua.ios_channel('b8f9b663-0a3b-cf45-587a-be880946e881')
        p.device_types = ua.device_types('ios')
        p.merge_data = ua.merge_data(
            template_id='ef34a8d9-0ad7-491c-86b0-aea74da15161',
            substitutions={
                'FIRST_NAME': 'Bob',
                'LAST_NAME': 'Smith',
                'TITLE': ''
            }
        )

        self.assertEqual(
            p.payload,
            {
                'device_types': ['ios'],
                'merge_data': {
                    'template_id': 'ef34a8d9-0ad7-491c-86b0-aea74da15161',
                    'substitutions': {
                        'FIRST_NAME': 'Bob',
                        'LAST_NAME': 'Smith',
                        'TITLE': ''
                    }
                },
                'audience': {
                    'ios_channel': 'b8f9b663-0a3b-cf45-587a-be880946e881'
                }
            }
        )

""" Notes for more template tests and docs

Lookup

In [3]: template = ua.TemplateInfo.lookup(airship, '230ab223-7cce-48d8-be28-46f717a42985')

In [4]: print (template.template_id, template.created_at, template.modified_at, template.last_used, template.name, template.description, template.variables, template.push)
(u'230ab223-7cce-48d8-be28-46f717a42985', datetime.datetime(2016, 6, 28, 19, 18, 0, 366000), datetime.datetime(2016, 6, 28, 19, 56, 31, 877000), datetime.datetime(2017, 8, 23, 23, 52, 1, 180000), u'Pet Sounds', u'What kind of animal noises do you like?', [{u'default_value': u'\U0001f434', u'name': u'Animal emoji', u'key': u'animal', u'description': u"The emoji of a user's animal."}, {u'default_value': u'Bob', u'name': u'First Name', u'key': u'first_name', u'description': u'First name of user.'}, {u'default_value': u'Neigh', u'name': u'Animal Noise', u'key': u'noise', u'description': u"The noise the user's animal makes."}], {u'notification': {u'android': {u'title': u'Pet Sounds {{animal}}', u'summary': u'{{animal}}'}, u'ios': {u'sound': u'cat.caf', u'badge': u'+1', u'title': u'Pet Sounds {{animal}}'}, u'actions': {u'open': {u'content': u'http://babygoatsandfriends.tumblr.com', u'type': u'deep_link'}}, u'alert': u'Hi {{ first_name }}, the {{ animal }} goes {{ noise }}!'}})

{"ok":true,"template":{"id":"230ab223-7cce-48d8-be28-46f717a42985","name":"Pet Sounds","description":"What kind of animal noises do you like?","variables":[{"key":"animal","name":"Animal emoji","description":"The emoji of a user's animal.","default_value":"🐴"},{"key":"first_name","name":"First Name","description":"First name of user.","default_value":"Bob"},{"key":"noise","name":"Animal Noise","description":"The noise the user's animal makes.","default_value":"Neigh"}],"created_at":"2016-06-28T19:18:00.366Z","modified_at":"2016-06-28T19:56:31.877Z","push":{"notification":{"android":{"summary":"{{animal}}","title":"Pet Sounds {{animal}}"},"ios":{"sound":"cat.caf","badge":"+1","title":"Pet Sounds {{animal}}"},"actions":{"open":{"content":"http://babygoatsandfriends.tumblr.com","type":"deep_link"}},"alert":"Hi {{ first_name }}, the {{ animal }} goes {{ noise }}!"}},"last_used":"2017-08-23T23:52:01.180Z"}}

Listing

# TODO: don't forget to test NEXTs (test for channel listing too why not)

In [5]: for template in ua.TemplateList(airship):
   ...:     template_id = template.template_id
   ...:     print (template.template_id, template.created_at, template.modified_at, template.last_used, template.name, template.description, template.variables, template.push)
"""
