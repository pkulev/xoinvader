"""Test xoinvader.__init__ module."""

import pytest

import xoinvader
from xoinvader.common import Settings
from xoinvader.utils import dotdict


# pylint: disable=missing-docstring
def test_init():
    Settings.system.test_section = dotdict(key="value")
    xoinvader.init()
    xoinvader.init({"test_section": dotdict(another_key="another-value")})
    assert Settings.system.test_section.another_key == "another-value"

    with pytest.raises(xoinvader.XOInitializationError):
        xoinvader.init("bad-value")

    with pytest.raises(xoinvader.XOInitializationError):
        xoinvader.init({"bad-key": "value"})
