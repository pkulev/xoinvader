import sys
import unittest
import pprint

from xoinvader.utils import Timer


class TestSettings(unittest.TestCase):
    def _func(self):
        self.check = True

    def test_timer_get_elapsed(self):
        self.check = False
        self.timer = Timer(5.0, self._func)
        self.timer.start()
        while self.timer.isRunning():
            self.assertGreaterEqual(self.timer.getElapsed(), 0.0,
                    msg="check={0}\n".format(str(self.check)) + pprint.pformat(vars(self.timer)))
            self.timer.update()
            self.assertGreaterEqual(self.timer.getElapsed(), 0.0,
                    msg="check={0}\n".format(str(self.check)) + pprint.pformat(vars(self.timer)))
