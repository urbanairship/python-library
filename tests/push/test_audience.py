import unittest

import urbanairship as ua


class TestAudience(unittest.TestCase):
    def test_basic_selectors(self):
        selectors = (
            (
                ua.ios_channel,
                "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3",
                {"ios_channel": "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3"},
            ),
            (
                ua.android_channel,
                "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3",
                {"android_channel": "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3"},
            ),
            (
                ua.amazon_channel,
                "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3",
                {"amazon_channel": "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3"},
            ),
            (
                ua.open_channel,
                "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3",
                {"open_channel": "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3"},
            ),
            (ua.device_token, "f" * 64, {"device_token": "F" * 64}),
            (ua.device_token, "0" * 64, {"device_token": "0" * 64}),
            (
                ua.apid,
                "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3",
                {"apid": "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3"},
            ),
            (
                ua.wns,
                "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3",
                {"wns": "074e84a2-9ed9-4eee-9ca4-cc597bfdbef3"},
            ),
            (ua.tag, "test", {"tag": "test"}),
            (ua.alias, "test", {"alias": "test"}),
            (ua.segment, "test", {"segment": "test"}),
        )

        for selector, value, result in selectors:
            self.assertEqual(selector(value), result)

    def test_sms_selectors(self):
        sms_id_selector = ua.sms_id("01230984567", "76543210")

        self.assertEqual(
            sms_id_selector, {"sms_id": {"sender": "76543210", "msisdn": "01230984567"}}
        )

        sms_sender_selector = ua.sms_sender("76543210")

        self.assertEqual(sms_sender_selector, {"sms_sender": "76543210"})

    def test_invalid_device_selectors(self):
        selectors = (
            (ua.ios_channel, "074e84a2-9ed9-4eee-9ca4-cc597bfdbef34"),
            (ua.android_channel, "074e84a2-9ed9-Beee-9ca4-ccc597bfdbef3"),
            (ua.amazon_channel, "074e84a2-Red9-5eee-0ca4-cc597bfdbef3"),
            (ua.open_channel, "074e84a2-OPEN-UP-0ca4-cc597bfdbef3"),
            (ua.device_token, "f" * 63),
            (ua.device_token, "f" * 65),
            (ua.device_token, "0123"),
            (ua.device_token, "X" * 64),
            (ua.apid, "foobar"),
            (ua.apid, "074e84a2-9ed9-4eee-9ca4-cc597bfdbef33"),
            (ua.apid, "074e84a2-9ed9-4eee-9ca4-cc597bfdbef"),
            (ua.wns, "074e84a2-9ed9-4eee-9ca4-cc597bfdbef"),
        )

        for selector, value in selectors:
            self.assertRaises(ValueError, selector, value)

    def test_compound_selectors(self):
        self.assertEqual(
            ua.or_(ua.tag("foo"), ua.tag("bar")),
            {"or": [{"tag": "foo"}, {"tag": "bar"}]},
        )

        self.assertEqual(
            ua.and_(ua.tag("foo"), ua.tag("bar")),
            {"and": [{"tag": "foo"}, {"tag": "bar"}]},
        )

        self.assertEqual(ua.not_(ua.tag("foo")), {"not": {"tag": "foo"}})


class TestAttributeSelectors(unittest.TestCase):
    def test_date_incorrect_operator_raises(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.date_attribute(attribute="test_attribute", operator="the_way_we_wont")

            self.assertEqual(
                err_ctx.message,
                "operator must be one of: 'is_empty', 'before', 'after', 'range', 'equals'",
            )

    def test_date_is_empty(self):
        selector = ua.date_attribute(attribute="test_attribute", operator="is_empty")

        self.assertEqual(
            selector, {"attribute": "test_attribute", "operator": "is_empty"}
        )

    # testing exception raising only on before. after and equals use same codepath
    def test_date_before_no_value_raises(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.date_attribute(
                attribute="test_attribute", operator="before", precision="years"
            )

            self.assertEqual(
                err_ctx.message,
                "value must be included when using the 'before' operator",
            )

    def test_date_before_no_precision_raises(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.date_attribute(
                attribute="test_attribute",
                operator="before",
                value="2021-11-03 12:00:00",
            )

            self.assertEqual(
                err_ctx.message,
                "precision must be included when using the 'before' operator",
            )

    def test_date_before(self):
        selector = ua.date_attribute(
            attribute="test_attribute",
            operator="before",
            value="2021-11-03 12:00:00",
            precision="years",
        )

        self.assertEqual(
            selector,
            {
                "attribute": "test_attribute",
                "operator": "before",
                "value": "2021-11-03 12:00:00",
                "precision": "years",
            },
        )

    def test_date_after(self):
        selector = ua.date_attribute(
            attribute="test_attribute",
            operator="after",
            value="2021-11-03 12:00:00",
            precision="years",
        )

        self.assertEqual(
            selector,
            {
                "attribute": "test_attribute",
                "operator": "after",
                "value": "2021-11-03 12:00:00",
                "precision": "years",
            },
        )

    def test_date_equals(self):
        selector = ua.date_attribute(
            attribute="test_attribute",
            operator="equals",
            value="2021-11-03 12:00:00",
            precision="years",
        )

        self.assertEqual(
            selector,
            {
                "attribute": "test_attribute",
                "operator": "equals",
                "value": "2021-11-03 12:00:00",
                "precision": "years",
            },
        )

    def test_text(self):
        selector = ua.text_attribute(
            attribute="test_attribute", operator="equals", value="test_value"
        )

        self.assertEqual(
            selector,
            {
                "attribute": "test_attribute",
                "operator": "equals",
                "value": "test_value",
            },
        )

    def test_text_incorrect_operator_raises(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.text_attribute(
                attribute="test_attribute", operator="am_180", value="test_value"
            )

            self.assertEqual(
                err_ctx.message,
                "operator must be one of 'equals', 'contains', 'less', 'greater', 'is_empty'",
            )

    def test_text_incorrect_value_type_raises(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.text_attribute(attribute="test_attribute", operator="am_180", value=2001)

            self.assertEqual(err_ctx.message, "value must be a string")

    def test_number(self):
        selector = ua.number_attribute(
            attribute="test_attribute", operator="equals", value=100
        )

        self.assertEqual(
            selector,
            {"attribute": "test_attribute", "operator": "equals", "value": 100},
        )

    def test_number_incorrect_operator_raises(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.number_attribute(
                attribute="test_attribute", operator="am_180", value="test_value"
            )

            self.assertEqual(
                err_ctx.message,
                "operator must be one of 'equals', 'contains', 'less', 'greater', 'is_empty'",
            )

    def test_number_incorrect_value_type_raises(self):
        with self.assertRaises(ValueError) as err_ctx:
            ua.number_attribute(
                attribute="test_attribute", operator="equals", value="ive_got_it"
            )

            self.assertEqual(err_ctx.message, "value must be an integer")
