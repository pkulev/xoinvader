import pytest

from xoinvader.settings import dotdict


def test_settings_setattr():
    settings = dotdict()
    settings.test_entry = 42
    assert settings["test_entry"] == 42
    assert settings.test_entry == 42

    settings["test_entry_2"] = 42
    assert settings.test_entry == 42

    assert pytest.raises(AttributeError, lambda: settings.bad_key)
