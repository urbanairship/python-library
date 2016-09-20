import unittest
import reach as ua
from reach.fields import Field


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

        base_payload = self.min_apple_field._build_common_json()
        self.assertEqual(
            extended_apple_json, self.min_apple_field.build_apple_json(
                base_payload
            )
        )
        self.assertEqual(
            self.full_apple_json[1], self.full_apple_field.build_apple_json(
                base_payload
            )
        )

    def test_build_google_json(self):
        extended_google_json = self.min_google_json[1].copy()
        extended_google_json.update({
            'order': 1,
            'formatType': 'String'
        })

        base_payload = self.min_apple_field._build_common_json()
        self.assertEqual(
            extended_google_json, self.min_google_field.build_google_json(
                base_payload
            )
        )
        self.assertEqual(
            self.full_google_json[1],
            self.full_google_field.build_google_json(
                base_payload
            )
        )

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
        self.assertEqual(
            Field._infer_format_type('http://google.com/cool_gif.gif'), 'URL'
        )
        self.assertEqual(
            Field._infer_format_type('2016-01-01T19:00:00Z'), 'Date'
        )

    def test_field_manipulations(self):
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
