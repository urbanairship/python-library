""" Pre-defined templates to be used in tests.
"""
import reach as ua


# Apple loyalty template
def build_apple_loyalty():
    template = ua.AppleTemplate()
    template.add_metadata(
        name='Loyalty Copy 7',
        description='With textAlignment, formatType, numberStyle, '
                    'fixed location, and order',
        project_type='memberCard',
        template_type='Store Card'
    )
    template.add_headers(
        suppress_strip_shine='true',
        barcode_value='123456789',
        icon_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-icon.png',
        barcode_type=ua.BarcodeType.PDF_417,
        logo_image='https://s3.amazonaws.com/passtools_prod/1/images/default-pass-logo.png',
        background_color=ua.rgb(49, 159, 196),
        barcode_encoding='iso-8859-1',
        logo_color=ua.rgb(24, 86, 148),
        barcodeAltText='123456789',
        foreground_color=ua.rgb(255, 255, 255),
        logo_text='Logo Text'
    )

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
        order=1
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

    template.add_fields(
        program_name,
        points,
        program_details,
        tier,
        merchant_website,
        tier_name,
        member_name
    )

    template.add_beacon(
        '3526dee6-4ea8-11e6-beb8-9e71128cae77',
        relevant_text='Look where you are!',
        major=123,
        minor=456
    )

    return template


# Build Google loyalty
def build_google_loyalty():
    template = ua.GoogleTemplate()

    template.add_metadata(
        name='Loyalty Copy',
        description='Loyalty description',
        template_type='Loyalty',
        project_type='loyalty'
    )

    template.add_headers(
        barcodeAltText='123456789',
        barcode_encoding='iso-8859-1',
        barcode_type=ua.BarcodeType.PDF_417,
        barcode_value='123456789'
    )

    # Account Module fields
    member_id = ua.Field(
        name='Member ID',
        fieldType=ua.GoogleFieldType.ACCOUNT_MODULE,
        value='123456789',
        label='Member ID',
        order=2
    )
    member_name = ua.Field(
        name='Member Name',
        fieldType=ua.GoogleFieldType.ACCOUNT_MODULE,
        value='First Last',
        label='Member Name',
        order=1
    )

    # Links module
    merchant_website = ua.Field(
        name='Merchant Website',
        label='Merchant Website',
        fieldType=ua.GoogleFieldType.LINKS_MODULE,
        value='http://www.test.com',
        order=1
    )

    # Points module
    program_points = ua.Field(
        name='Program Points',
        label='Program Points',
        fieldType=ua.GoogleFieldType.POINTS_MODULE,
        value='250',
        order=1
    )

    tier = ua.Field(
        name='Tier',
        label='Tier',
        fieldType=ua.GoogleFieldType.POINTS_MODULE,
        value='2.0',
        order=2
    )

    # Text module
    program_details = ua.Field(
        name='Program Details',
        label='Program Details',
        fieldType=ua.GoogleFieldType.TEXT_MODULE,
        value='Some information about how the loyalty program works.',
        order=1
    )

    # Title module
    loyalty_program = ua.Field(
        name='Loyalty Program Name',
        label='Bleep',
        fieldType=ua.GoogleFieldType.TITLE_MODULE,
        value='Loyalty Program Name',
        order=1
    )

    template.add_fields(
        member_id,
        member_name,
        merchant_website,
        program_points,
        tier,
        program_details,
        loyalty_program
    )

    return template
