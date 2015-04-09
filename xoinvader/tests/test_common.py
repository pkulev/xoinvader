import sys
import unittest

from xoinvader.common import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

    def tearDown(self):
        del self.settings

    def test_setattr(self):
        settings = Settings()
        settings.test_thing = 42
        self.assertEquals(42, settings._settings["test_thing"])

    def test_getattr(self):
        settings = Settings()
        settings._settings["test_thing"] = 42
        self.assertEquals(42, settings.test_thing)

    def test_setattr_with_getattr(self):
        settings = Settings()
        settings.test_thing = 42
        self.assertEquals(42, settings.test_thing)
    @unittest.skip
    def test_get_nonexistent_value(self):
        pass
