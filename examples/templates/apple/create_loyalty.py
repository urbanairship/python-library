import reach as ua
import os
import json


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])


# Step 1: Create the template and add top-level values
apple_loyalty = ua.AppleTemplate()

apple_loyalty.add_metadata(
    name='Beacon Test',
    description='With textAlignment, formatType, numberStyle, fixed location, and order',
    type_=ua.Type.LOYALTY
)


# Step 2: Add headers
apple_loyalty.add_headers(
    suppress_strip_shine='',
    barcode_value='123456789',
    icon_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-icon.png',
    barcode_type=ua.BarcodeType.PDF_417,
    logo_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-logo.png',
    background_color=ua.rgb(49,159,196),
    logo_color=ua.rgb(24,86,148),
    barcodeAltText='123456789',
    foreground_color=ua.rgb(255,255,255),
    barcode_encoding='iso-8859-1',
    strip_image=''
)


# Step 3: Create and add fields
program_name = ua.Field(
    name='Program Name',
    label='Bleep',
    value='Program Name',
    fieldType=ua.AppleFieldType.PRIMARY,
)

points = ua.Field(
    name='Points',
    label='Points',
    value=1234.0,
    fieldType=ua.AppleFieldType.HEADER,
)

program_details = ua.Field(
    name='Program Details',
    label='Program Details',
    value='Some info about how the loyalty program works and its benefits',
    fieldType=ua.AppleFieldType.BACK,
    order=1,
    changeMessage=None,
    hideEmpty=False,
    required=False
)

tier = ua.Field(
    name='Tier',
    label='Tier',
    value=2.0,
    fieldType=ua.AppleFieldType.SECONDARY,
    order=1
)

merchant_website = ua.Field(
    name='Merchant Website',
    label='Merchant Website',
    value='http://www.test.com',
    fieldType=ua.AppleFieldType.BACK,
    formatType='URL',
    order=2
)

tier_name = ua.Field(
    name='Tier Name',
    label='Tier Name',
    value='Silver',
    fieldType=ua.AppleFieldType.SECONDARY,
    order=2
)

member_name = ua.Field(
    name='Member Name',
    label='Member Name',
    value='First Last',
    fieldType=ua.AppleFieldType.SECONDARY,
    order=3
)

apple_loyalty.add_fields(
    program_name,
    points,
    program_details,
    tier,
    merchant_website,
    tier_name,
    member_name
)

print json.dumps(apple_loyalty._create_payload(), sort_keys=True, indent=4)
response = apple_loyalty.create(ua_reach, project_id=51597)
print response
