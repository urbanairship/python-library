import urbanairship_reach as ua


def build_apple_pass():
    pass_ = ua.ApplePass()
    pass_.metadata = {
        'id': '18971172',
        'templateId': '51234',
        'status': 'not_been_installed',
        'tags': []
    }
    pass_.add_headers(
        barcode_encoding='iso-8859-1'
    )

    points = ua.Field(
        name='Points',
        fieldType='primary',
        numberStyle='numberStyleDecimal',
        value=33.0
    )

    pass_.add_fields(points)
    return pass_


def build_google_pass():
    pass_ = ua.GooglePass()
    pass_.metadata = {
        'id': '18971172',
        'templateId': '51234',
        'status': 'not_been_installed',
        'tags': []
    }
    pass_.add_headers(
        barcode_encoding='iso-8859-1'
    )

    points = ua.Field(
        name='Points',
        fieldType=ua.GoogleFieldType.POINTS_MODULE,
        value=33.0
    )

    pass_.add_fields(points)
    return pass_
