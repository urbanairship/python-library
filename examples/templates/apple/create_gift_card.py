import reach as ua
import os
import json


ua_reach = ua.Reach(os.environ['PERSONAL_EMAIL'], os.environ['REACH_KEY_RAW'])


# Step 1: Create the template and add top-level values
apple_gift_card = ua.AppleTemplate()


apple_gift_card.add_metadata(
    name='Gift Card Clone 1',
    description='A lil\' description',
    project_type='giftCard',
    template_type='Store Card'
)

# Step 2: Add headers.
apple_gift_card.add_headers(
    barcode_value='123456789',
    icon_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-icon.png',
    barcode_type=ua.BarcodeType.PDF_417,
    logo_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-logo.png',
    background_color=ua.rgb(0, 147, 201),
    barcode_encoding='iso-8859-1',
    logo_color=ua.rgb(24, 86, 148),
    barcodeAltText='123456789',
    foreground_color=ua.rgb(255, 255, 255),
    strip_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-strip.png',
    logo_text='Bleep'
)

# Step 3: Create and add fields.
merchant_id = ua.Field(
    name='Merchant ID',
    label='Merchant ID',
    value='FG7AP4G',
    fieldType=ua.AppleFieldType.SECONDARY,
    order=2
)

card_name = ua.Field(
    name='Card Name',
    label='Card Name',
    value='Bleep',
    fieldType=ua.AppleFieldType.HEADER
)

card_id = ua.Field(
    name='Card ID',
    label='Card ID',
    value=123456789.0,
    fieldType=ua.AppleFieldType.SECONDARY
)

merchant_website = ua.Field(
    name='Merchant Website',
    label='Merchant Website',
    value='http://www.test.com',
    fieldType=ua.AppleFieldType.BACK,
    order=2
)

gift_card_details = ua.Field(
    name='Gift Card Details',
    label='Gift Card Details',
    value='Some info about this gift card',
    fieldType=ua.AppleFieldType.BACK
)

balance = ua.Field(
    name='Balance',
    label='Balance',
    value=19.78,
    formatType='Currency',
    currencyCode='USD',
    fieldType=ua.AppleFieldType.PRIMARY
)

apple_gift_card.add_fields(
    merchant_id,
    card_name,
    card_id,
    merchant_website,
    gift_card_details,
    balance
)

print json.dumps(apple_gift_card._create_payload(), sort_keys=True, indent=4)
response = apple_gift_card.create(ua_reach, project_id=50784)
print response
