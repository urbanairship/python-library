import unittest
import uareach as ua
from uareach.fields import Field


class TestField(unittest.TestCase):
    def setUp(self):
        self.min_apple_json = ('Member Name', {
            'fieldType': 'primary',
            'label': 'Member Name',
            'value': 'First Last'
        })
        self.min_apple_field = Field(
            name='Member Name',
            label='Member Name',
            value='First Last',
            fieldType=ua.AppleFieldType.PRIMARY
        )
        self.min_google_json = ('Member Name', {
            'label': 'Member Name',
            'value': 'First Last',
            'fieldType': ua.GoogleFieldType.INFO_MODULE
        })
        self.min_google_field = Field(
            name='Member Name',
            label='Member Name',
            value='First Last',
            fieldType=ua.GoogleFieldType.INFO_MODULE
        )

        self.full_apple_json = ('Member Name', {
            'fieldType': 'primary',
            'changeMessage': 'Things change',
            'formatType': 'String',
            'hideEmpty': True,
            'label': 'Member Name',
            'order': 2,
            'required': False,
            'value': 'First Last',
            'textAlignment': 'textAlignmentRight'
        })
        self.full_apple_field = Field(
            name='Member Name',
            fieldType=ua.AppleFieldType.PRIMARY,
            changeMessage='Things change',
            formatType='String',
            hideEmpty=True,
            label='Member Name',
            order=2,
            required=False,
            value='First Last',
            textAlignment='textAlignmentRight'
        )
        self.full_google_json = ('Member Name', {
            'order': 0,
            'label': 'Member Name',
            'value': 'Taylor Lakehurst',
            'fieldType': ua.GoogleFieldType.ACCOUNT_MODULE,
            'formatType': 'String',
            'changeMessage': None,
            'hideEmpty': False,
            'required': False
        })
        self.full_google_field = Field(
            order=0,
            name='Member Name',
            label='Member Name',
            value='Taylor Lakehurst',
            fieldType=ua.GoogleFieldType.ACCOUNT_MODULE,
            formatType='String',
            changeMessage=None,
            hideEmpty=False,
            required=False
        )

    def test_build_apple_field(self):
        self.assertEqual(
            Field.build_apple_field(
                self.min_apple_json[0], self.min_apple_json[1]
            ), self.min_apple_field
        )
        self.assertEqual(
            Field.build_apple_field(
                self.full_apple_json[0], self.full_apple_json[1]
            ), self.full_apple_field
        )

    def test_build_google_field(self):
        self.assertEqual(
            Field.build_google_field(
                self.min_google_json[0], self.min_google_json[1]
            ), self.min_google_field
        )
        self.assertEqual(
            Field.build_google_field(
                self.full_google_json[0], self.full_google_json[1]
            ), self.full_google_field
        )

    def test_build_apple_json(self):
        extended_apple_json = self.min_apple_json[1].copy()
        extended_apple_json.update({
            'order': 1,
            'formatType': 'String'
        })

        self.min_apple_field._build_common_template_json()
        self.assertEqual(
            extended_apple_json, self.min_apple_field.build_apple_json()
        )
        self.assertEqual(
            self.full_apple_json[1], self.full_apple_field.build_apple_json()
        )

    def test_build_google_json(self):
        extended_google_json = self.min_google_json[1].copy()
        extended_google_json.update({
            'order': 1,
            'formatType': 'String'
        })

        self.min_google_field._build_common_template_json()
        self.assertEqual(
            extended_google_json, self.min_google_field.build_google_template_json()
        )
        self.assertEqual(
            self.full_google_json[1], self.full_google_field.build_google_template_json()
        )

    def test_build_generic_json(self):
        field = Field(name='Member Name', value='First Last')
        payload = field.build_pass_json()
        self.assertEquals(payload, {'value': 'First Last'})

        google_field = Field(
            name='Test', fieldType=ua.GoogleFieldType.TEXT_MODULE, value='Hello'
        )
        payload = google_field.build_pass_json()
        self.assertEquals(payload, {'fieldType': 'textModulesData', 'value': 'Hello'})

        apple_field = Field(
            name='Test', fieldType=ua.AppleFieldType.PRIMARY, formatType='Number', value=1234
        )
        payload = apple_field.build_pass_json()
        self.assertEquals(
            payload,
            {
                'formatType': 'Number',
                'value': 1234,
                'fieldType': 'primary',
                'numberStyle': 'numberStyleDecimal'
            }
        )

    def test_build_common_json(self):
        # Test setting Currency formatType
        field = Field(name='Value', currencyCode='USD')
        field._build_common_template_json()
        self.assertEquals(field.field_values['formatType'], 'Currency')

        # Test that infer_format_type is triggered
        field = Field(name='Member Name', value='Hello there')
        field._build_common_template_json()
        self.assertEquals(field.field_values['formatType'], 'String')

        # Test that order and fieldType are set
        field = Field(name='Member Name')
        field._build_common_template_json()
        self.assertEquals(field.field_values['order'], 1)
        self.assertEquals(field.field_values['fieldType'], 'notAssigned')

    def test_infer_number_style(self):
        self.assertEqual(
            Field._infer_number_style(1234), ua.NumberStyle.DECIMAL
        )
        self.assertEqual(
            Field._infer_number_style(1234.0142), ua.NumberStyle.DECIMAL
        )
        self.assertEqual(
            Field._infer_number_style('1234'), ua.NumberStyle.TEXT
        )
        self.assertEqual(
            Field._infer_number_style('1234e2'), ua.NumberStyle.SCIENTIFIC
        )
        self.assertEqual(
            Field._infer_number_style('1234E2'), ua.NumberStyle.SCIENTIFIC
        )
        self.assertRaises(ValueError, Field._infer_number_style, {})

    def test_row_col_to_order(self):
        self.assertEqual(Field._row_col_to_order(0, 0), 1)
        self.assertEqual(Field._row_col_to_order(1, 0), 2)
        self.assertEqual(Field._row_col_to_order(0, 1), 2)
        row_col_data = {
            'row': 0,
            'col': 1,
            'label': 'Member Name',
            'value': 'Taylor Lakehurst',
            'fieldType': 'acctModule',
            'formatType': 'String'
        }
        row_col_field = Field.build_google_field('Member Name', row_col_data)
        self.assertEqual(row_col_field['order'], 2)
        self.assertIsNone(row_col_field.get('row', None))
        self.assertIsNone(row_col_field.get('col', None))

    def test_infer_format_type(self):
        self.assertEqual(Field._infer_format_type('Hello'), 'String')
        self.assertEqual(Field._infer_format_type(1234), 'Number')
        self.assertEqual(Field._infer_format_type(123.321), 'Number')
        self.assertEqual(Field._infer_format_type('123.01'), 'Number')
        self.assertEqual(Field._infer_format_type('123'), 'Number')
        self.assertEqual(Field._infer_format_type('1.233e4'), 'Number')
        self.assertEqual(
            Field._infer_format_type('http://google.com/cool_gif.gif'), 'URL'
        )
        self.assertEqual(
            Field._infer_format_type('2016-01-01T19:00:00Z'), 'Date'
        )
        self.assertRaises(ValueError, Field._infer_format_type, {})

    def test_setitem(self):
        gf = Field(
            name='Member Name',
            fieldType=ua.GoogleFieldType.TEXT_MODULE
        )
        af = Field(
            name='Member Name',
            fieldType=ua.AppleFieldType.PRIMARY
        )
        # Test google field label/value conversions
        gf['header'] = 'Hello hello'
        gf['body'] = 'This is the body'
        self.assertEquals(gf['label'], 'Hello hello')
        self.assertEquals(gf['value'], 'This is the body')
        # Test invalid key
        self.assertRaises(ValueError, gf.__setitem__, 'doesntExist', 'Who Cares?')
        # Test invalid values
        self.assertRaises(ValueError, af.__setitem__, 'textAlignment', 'blah')
        self.assertRaises(ValueError, af.__setitem__, 'formatType', 'bool')
        self.assertRaises(ValueError, af.__setitem__, 'numberStyle', 'wrong')
        # Test numberStyle replacement
        af['numberStyle'] = 'PKNumberStyleDecimal'
        self.assertEquals(af['numberStyle'], 'numberStyleDecimal')
        # Test loyaltyPoints replacement
        gf['fieldType'] = ua.GoogleFieldType._LOYALTY_POINTS
        self.assertEquals(gf['fieldType'], ua.GoogleFieldType.POINTS_MODULE)

    def test_other_field_manipulations(self):
        f = Field(
            name='Member Name',
            label='Member Name',
            value='First Last',
            fieldType=ua.AppleFieldType.PRIMARY
        )
        f['label'] = 'Updated Member Name'
        f['formatType'] = 'String'
        updated_f = Field(
            name='Member Name',
            label='Updated Member Name',
            value='First Last',
            formatType='String',
            fieldType=ua.AppleFieldType.PRIMARY
        )
        self.assertEqual(f, updated_f)
        del f['formatType']
        updated_f = Field(
            name='Member Name',
            label='Updated Member Name',
            value='First Last',
            fieldType=ua.AppleFieldType.PRIMARY
        )
        self.assertEqual(f, updated_f)
        self.assertEqual(len(f), 3)

