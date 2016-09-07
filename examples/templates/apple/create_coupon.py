import wallet as ua
import os
import json


ua_wallet = ua.Wallet(os.environ['PERSONAL_EMAIL'], os.environ['WALLET_KEY_RAW'])


# Step 1: Create the template and add top-level values
apple_coupon = ua.AppleTemplate()

apple_coupon.add_metadata(
    name='Coupon Clone 1',
    description='A lil\' description',
    project_type='coupon',
    template_type='Coupon'
)

# 2. Set headers
apple_coupon.add_headers(
    barcode_value='123456789',
    icon_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-icon.png',
    barcode_type=ua.BarcodeType.AZTEC,
    logo_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-logo.png',
    background_color=ua.rgb(0, 147, 201),
    barcode_encoding='iso-8859-1',
    logo_color=ua.rgb(24, 86, 148),
    barcodeAltText='123456789',
    foreground_color=ua.rgb(255, 255, 255),
    strip_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-strip.png',
    logo_text='Bleep'
)

# 3. Create and add fields.
merchant_website = ua.Field(
    name='Merchant Website',
    label='Merchant Website',
    value='http://www.test.com',
    fieldType=ua.AppleFieldType.BACK,
    formatType='URL',
    order=2
)

coupon_details = ua.Field(
    name='Coupon Details',
    label='Coupon Details',
    value='Some info about how to use this Coupon',
    fieldType=ua.AppleFieldType.BACK,
    order=1
)

coupon_title = ua.Field(
    name='Coupon Title',
    label='20% Discount',
    value='Coupon',
    fieldType=ua.AppleFieldType.PRIMARY,
)

valid_thru = ua.Field(
    name='Valid Through',
    label='Valid Through',
    value='June 25, 2013',
    fieldType=ua.AppleFieldType.SECONDARY,
    order=1
)

coupon_num = ua.Field(
    name='Coupon #',
    label='Coupon #',
    value=4917635.0,
    fieldType=ua.AppleFieldType.SECONDARY,
    order=2
)

location = ua.Field(
    name='Location',
    label='Location',
    value='All Stores',
    fieldType=ua.AppleFieldType.HEADER,
)

apple_coupon.add_fields(
    merchant_website,
    coupon_details,
    coupon_title,
    valid_thru,
    coupon_num,
    location
)


print json.dumps(apple_coupon._create_payload(), sort_keys=True, indent=4)
response = apple_coupon.create(ua_wallet, project_id=50783)
print response
