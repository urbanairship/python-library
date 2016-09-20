import reach as ua
from reach import GoogleFieldType
import os
import json


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])

google_loyalty = ua.GoogleTemplate()


google_loyalty.add_metadata(
    name='Loyalty Copy',
    description='Loyalty description',
    type_=ua.Type.LOYALTY
)

google_loyalty.add_headers(
    barcodeAltText='123456789',
    barcode_encoding='iso-8859-1',
    barcode_type='PDF_417',
    barcode_value='123456789'
)

# Account Module fields
member_id = ua.Field(
    name='Member ID',
    fieldType=GoogleFieldType.ACCOUNT_MODULE,
    value='123456789',
    label='Member ID',
    order=2
)
member_name = ua.Field(
    name='Member Name',
    fieldType=GoogleFieldType.ACCOUNT_MODULE,
    value='First Last',
    label='Member Name',
    order=1
)

# Links module
merchant_website = ua.Field(
    name='Merchant Website',
    label='Merchant Website',
    fieldType=GoogleFieldType.LINKS_MODULE,
    value='http://www.test.com',
    order=1
)

# Points module
program_points = ua.Field(
    name='Program Points',
    label='Program Points',
    fieldType=GoogleFieldType.POINTS_MODULE,
    value='250',
    order=1
)

tier = ua.Field(
    name='Tier',
    label='Tier',
    fieldType=GoogleFieldType.POINTS_MODULE,
    value='2.0',
    order=2
)

# Text module
program_details = ua.Field(
    name='Program Details',
    label='Program Details',
    fieldType=GoogleFieldType.TEXT_MODULE,
    value='Some information about how the loyalty program works.',
    order=1
)

# Title module
loyalty_program = ua.Field(
    name='Loyalty Program Name',
    label='Bleep',
    fieldType=GoogleFieldType.TITLE_MODULE,
    value='Loyalty Program Name',
    order=1
)

google_loyalty.add_fields(
    member_id,
    member_name,
    merchant_website,
    program_points,
    tier,
    program_details,
    loyalty_program
)

# Top level headers
google_loyalty.add_top_level_fields(
    GoogleFieldType.TITLE_MODULE,
    image='https://s3.amazonaws.com/passtools_prod/1/images/default-loyalty-logo.png',
    imageDescription=''
)

google_loyalty.add_message(
    body='Testing 1, 2'
)

print json.dumps(google_loyalty._create_payload(), sort_keys=True, indent=4)
response = google_loyalty.create(ua_reach, project_id=50785)
print response
