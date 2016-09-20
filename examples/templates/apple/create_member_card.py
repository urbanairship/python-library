import reach as ua
import os
import json


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])


# Step 1: Create the template and add top-level values
apple_member_card = ua.AppleTemplate()

apple_member_card.add_metadata(
    name='Member Card Copy',
    description='Descriptionzzzzz',
    project_type='memberCard',
    template_type='Generic'
)

# Step 2: Add headers
apple_member_card.add_headers(
    barcode_value='123456789',
    icon_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-icon.png',
    barcode_type=ua.BarcodeType.PDF_417,
    logo_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-logo.png',
    thumbnail_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-thumbnail.png',
    background_color=ua.rgb(0,147,201),
    barcode_encoding='iso-8859-1',
    logo_color=ua.rgb(24,86,148),
    barcodeAltText='123456789',
    foreground_color=ua.rgb(255,255,255),
    logo_text='Logo Text'
)

# Step 3: Create and add fields
program_name = ua.Field(
    name='Program Name',
    label='Program Name',
    value='Bleep',
    fieldType=ua.AppleFieldType.PRIMARY
)

merchant_id = ua.Field(
    name='Merchant ID',
    label='Merchant ID',
    value='FG7AP4G',
    fieldType=ua.AppleFieldType.SECONDARY,
    order=2
)

program_details = ua.Field(
    name='Program Details',
    label='Program Details',
    value='Some info about the member card n shit.',
    fieldType=ua.AppleFieldType.BACK,
    order=2
)

card_id = ua.Field(
    name='Card ID',
    label='Card ID',
    value=1262662.0,
    fieldType=ua.AppleFieldType.HEADER
)

merchant_website = ua.Field(
    name='Merchant Website',
    label='Merchant Website',
    value='http://www.test.com',
    fieldType=ua.AppleFieldType.BACK
)

member_name = ua.Field(
    name='Member Name',
    label='Member Name',
    value='First Last',
    fieldType=ua.AppleFieldType.SECONDARY
)

apple_member_card.add_fields(
    program_name,
    merchant_id,
    program_details,
    card_id,
    merchant_website,
    member_name
)

print json.dumps(apple_member_card._create_payload(), sort_keys=True, indent=4)
response = apple_member_card.create(ua_reach, project_id=50866)
print response
