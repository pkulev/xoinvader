"""Keys' integer representation."""

import six

from xoinvader.utils import Singleton


K_A = ord("a")
K_D = ord("d")
K_E = ord("e")
K_F = ord("f")
K_N = ord("n")
K_R = ord("r")
K_S = ord("s")
K_Q = ord("q")
K_W = ord("w")
K_SPACE = ord(" ")
K_ESCAPE = 27
K_ENTER = 343


@six.add_metaclass(Singleton)
class _KEY(object):
    """Convenient key container with dot access.

    K_KEYNAME can be accessed via KEY.KEYNAME.
    .. Attention:: this class relies to K_{KEYNAME} scheme.
                   No more than one underscore allowed.
    """

    KEY_PREFIX = "K_"
    """Prefix for all keys."""

    def __init__(self):
        for key, scancode in globals().items():
            if key.startswith(self.KEY_PREFIX):
                self.__dict__[key.split("_")[1]] = scancode


KEY = _KEY()
"""Key container object."""
