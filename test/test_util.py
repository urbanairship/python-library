import unittest

from wallet import util


class TestEnum(unittest.TestCase):
    def test_validate(self):
        class ExampleEnum(util.Constant):
            KEY1 = 'value1'
            KEY2 = 'value2'
            _PRIVATE_KEY = 'privatevalue'

        ExampleEnum.validate('value1')
        ExampleEnum.validate('value2')
        self.assertRaises(ValueError, ExampleEnum.validate, 'value3')
        self.assertRaises(ValueError, ExampleEnum.validate, 'privatevalue')
