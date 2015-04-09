import sys
import unittest

sys.path.append("/home/pkulev/proj/xoinvader")

from xoinvader import Settings

class TestSettings(unittest.TestCase):
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
