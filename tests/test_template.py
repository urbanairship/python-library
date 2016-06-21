import json
import mock
import requests
import unittest

import wallet as ua


class TestTemplate(unittest.TestCase):
    def test_get_template(self):
        with mock.patch.object(ua_wallet.Wallet, '_request') as mock_request:
            response = requests.Response()
            response._content = json.dumps([
                {
                    # TODO json elsewhere
                    "fieldsModel": {
                        "headers": {
                            "logo_color": {
                                "formatType": 1,
                                "fieldType": "topLevel",
                                "value": "rgb(24,86,148)"
                            },
                            "icon_image": {
                                "formatType": 1,
                                "fieldType": "image",
                                "value": "https:\/\/s3.amazonaws.com\/passtools_prod\/1\/images\/default-pass-icon.png"
                            },
                            "logo_text": {
                                "formatType": 1,
                                "fieldType": "topLevel",
                                "value": "Logo Text"
                            },
                            "barcode_encoding": {
                                "formatType": 1,
                                "fieldType": "topLevel",
                                "value": "iso-8859-1"
                            },
                            "suppress_strip_shine": {
                                "formatType": 1,
                                "fieldType": "topLevel",
                                "value": "true"
                            },
                            "logo_image": {
                                "formatType": 1,
                                "fieldType": "image",
                                "value": "https:\/\/s3.amazonaws.com\/passtools_prod\/1\/images\/default-pass-logo.png"
                            },
                            "foreground_color": {
                                "formatType": 1,
                                "fieldType": "topLevel",
                                "value": "rgb(255,255,255)"
                            },
                            "background_color": {
                                "formatType": 1,
                                "fieldType": "topLevel",
                                "value": "rgb(49,159,196)"
                            }
                        },
                        "fields": {
                            "Text": {
                                "formatType": "String",
                                "changeMessage": "Edited",
                                "order": 1,
                                "fieldType": "primary",
                                "textAlignment": "textAlignmentRight",
                                "value": "",
                                "label": "Text",
                                "required": "false",
                                "hideEmpty": "true"
                            },
                            "spelledOut": {
                                "formatType": "String",
                                "changeMessage": "888",
                                "order": 2,
                                "numberStyle": "PKNumberStyleSpellOut",
                                "fieldType": "secondary",
                                "value": 888.0,
                                "label": "Spelled Out Edited",
                                "required": "false",
                                "hideEmpty": "true"
                            },
                            "Apple 2": {
                                "formatType": "String",
                                "changeMessage": "888",
                                "order": 1,
                                "fieldType": "secondary",
                                "value": "",
                                "label": "Apple 2",
                                "required": "false",
                                "hideEmpty": "false"
                            }
                        }
                    },
                    "templateHeader": {
                        "vendor": "Apple",
                        "projectType": "memberCard",
                        "projectId": 10057,
                        "type": "Store Card",
                        "vendorId": 1,
                        "deleted": "False",
                        "id": "23593",
                        "updatedAt": "2013-07-01T18:28:33.000Z",
                        "description": "Description",
                        "createdAt": "2013-07-01T18:28:33.000Z",
                        "name": "Loyalty Card",
                        "disabled": "False"
                    }
                }
            ]).encode('utf-8')
            response.status_code = 200
            mock_request.return_value = response

            my_wallet = ua.Wallet("email", "api_key")
            template = ua.AppleTemplate.get_from_id(my_wallet, "template_id")
            rearranged_for_upload = template.create_payload()

            # still working on this
            self.assertEqual(
                rearranged_for_upload["headers"],
                template["fieldModels"]["headers"]
            )
            self.assertEqual(
                rearranged_for_upload["fields"],
                template["fieldsModel"]["fields"]
            )
            self.assertEqual(
                rearranged_for_upload["key"],
                template["templateHeaders"]["each key here"]
            )

