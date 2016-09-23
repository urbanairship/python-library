import unittest

from uareach import util


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


def example_function():
    """Here are some docs"""
    return True


@util.set_docstring(example_function)
def example_function_no_docs():
    return False


class WithDocs(object):

    def __init__(self):
        pass

    def method_1(self):
        """method 1 docs"""
        return True

    def method_2(self):
        """method 2 docs"""
        return True

    def method_3(self):
        """method 3 docs"""
        return True


@util.inherit_docs
class WithoutDocs(WithDocs):

    def __init__(self):
        pass

    def method_1(self):
        return True

    def method_2(self):
        return True

    def method_3(self):
        """this method 3 is different"""
        return False


class TestDocs(unittest.TestCase):

    def test_set_docstring(self):
        self.assertEquals(
            example_function.__doc__, example_function_no_docs.__doc__
        )

    def test_inherit_docs(self):
        self.assertEquals(
            WithDocs.method_1.__doc__, WithoutDocs.method_1.__doc__
        )

        self.assertEqual(
            WithDocs.method_2.__doc__, WithoutDocs.method_2.__doc__
        )

        self.assertEquals(
            WithoutDocs.method_3.__doc__, "this method 3 is different"
        )
