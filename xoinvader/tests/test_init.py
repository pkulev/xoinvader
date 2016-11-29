import pytest

import xoinvader
from xoinvader.common import Settings
from xoinvader.utils import dotdict


def test_init():
    Settings.system.test_section = dotdict(key="value")
    xoinvader.init({"test_section": dotdict(another_key="another-value")})
    assert "another-value" == Settings.system.test_section.another_key

    with pytest.raises(xoinvader.XOInitializationError):
        xoinvader.init("bad-value")
