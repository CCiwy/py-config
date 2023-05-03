import os
from unittest import TestCase

from configparser import Config


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


class TestConfig(TestCase):

    def setUp(self):
        self.app = App()
        fp = f'{__file__.rsplit(".", 1)[0]}.py'
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

