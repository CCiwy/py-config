import os
from unittest import TestCase

from src.configparser import Config


class App:
    """ Test app, wrapper to init config """
    def __init__(self):
        self.config = Config()

# config keys used for testconfig
TEST_KEY = 'TEST_VALUE'
TEST_INT = 1
TEST_FLOAT = 1.0
TEST_BOOL = True
TEST_ENV = os.getenv('TEST_ENV', 'NOT IN ENV')

class TestMappingConfig(TestCase):
    def setUp(self) -> None:
        self.app = App()

        settings = {
            "dictkey" : 1,
            "dictnested" : {"sth" : "else"},
            "FLOAT" : 11234123.0
        }

        self.app.config.from_dict(settings)

    def test_lowercasekey_converted_to_upper(self):
        self.assertTrue("DICTKEY" in self.app.config)

    def test_float_not_parsed_as_string(self):
        self.assertIsInstance(self.app.config.FLOAT, float)


    def test_nested_values_get_parsed(self):
        self.assertTrue(self.app.config.DICTNESTED.get('sth', False))

class TestJSONFileConfig(TestCase):
    def setUp(self):
        self.app = App()
        fp = 'test.json'
        self.app.config.from_json(fp)
        print(self.app.config.NESTED)
        print(type(self.app.config.NESTED))


    def test_json_keys_in_config(self):
        self.assertTrue('CONFIG_VERSION' in self.app.config)


    def test_lowercasekey_converted_to_upper(self):
        self.assertTrue("LOWERCASEKEY" in self.app.config)


    def test_nested_values_get_parsed(self):
        self.assertTrue(self.app.config.NESTED.get("level2", False), self.app.config.NESTED)

class TestPyFileConfig(TestCase):

    def setUp(self):
        self.app = App()
        fp = f'{__file__.rsplit(".", 1)[0]}.py'
        print(self.app.config)
        self.app.config.from_pyfile(fp)

    def test_config_stores_key_as_dict_value_string(self):
        self.assertEqual(self.app.config["TEST_KEY"], TEST_KEY)


    def test_config_stores_key_as_dict_value_bool(self):
        self.assertIsInstance(self.app.config["TEST_BOOL"], bool)


    def test_config_stores_key_as_dict_value_float(self):
        self.assertIsInstance(self.app.config["TEST_FLOAT"], float)


    def test_config_stores_key_as_attr_string(self):
        self.assertEqual(self.app.config.TEST_KEY, TEST_KEY)


    def test_config_stores_key_as_dict_value_from_env(self):
        #note: since no env vars are set returns default
        self.assertEqual(self.app.config["TEST_ENV"], "NOT IN ENV")


    def test_config_stores_key_as_attr_bool(self):
        self.assertEqual(self.app.config.TEST_BOOL, TEST_BOOL)

