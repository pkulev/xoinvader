import sys
import unittest

from xoinvader.common import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

    def tearDown(self):
        del self.settings

    def test_setattr(self):
        self.settings.test_thing = 42
        self.assertEquals(42, self.settings["test_thing"])

    def test_getattr(self):
        self.settings["test_thing"] = 42
        self.assertEquals(42, self.settings.test_thing)

    def test_setattr_with_getattr(self):
        self.settings.test_thing = 42
        self.assertEquals(42, self.settings.test_thing)

    def test_get_nonexistent_value(self):
        self.assertRaises(KeyError, lambda : self.settings.test_thing)
