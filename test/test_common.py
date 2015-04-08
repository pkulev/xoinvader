import sys
import unittest

from xoinvader import Settings

class TestSettings(unittest.TestCase):
    def test_setattr(self):
        settings = Settings()
        settings.test_thing = 42
        self.AssertEquals(42, settings["test_thing"])

    def test_getattr(self):
        settings = Settings()
        settings["test_thing"] = 42
        self.AssertEquals(42, settings.test_thing)

    def test_setattr_with_getattr(self):
        settings = Settings()
        settings.test_thing = 42
        self.AssertEquals(42, settings.test_thing)
   
