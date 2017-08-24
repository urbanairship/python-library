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
