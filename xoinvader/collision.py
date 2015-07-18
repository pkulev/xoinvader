"""Collision detection."""


class SettingsManager(object):
    def __init__(self, settings_map={}):
        self._smap = settings_map

    def notify(self, owner, settings):
        self._smap[owner].update(settings)


class UpdatableSettings(object):
    def __init__(self, settings_manager, settings={}):
        self._settings = settings
        self._settings_manager = settings_manager

    def updateInstanceSettings(self, settings):
        self._settings.update(settings)

    def notifySettingsManager(self):
        self._settings_manager.notify(self.__class__.__name__, settings)


class CollisionDetector(UpdatableSettings):
    def __init__(self, settings={}):
        self._settings = settings


if __name__ == "__main__":
    from settings import dotdict

    settings = dotdict({
        "setting1": True,
        "setting2": 50,
        "setting3": "Disabled"
    })

    settings_manager = SettingsManager({"UpdatableSettings": settings.copy()})
    print(settings_manager._smap)
    s1 = UpdatableSettings(settings_manager, settings)
    print(s1._settings)
    s1.updateInstanceSettings({"Lolo": 5})
    print(s1._settings)
    print(settings_manager._smap)
    s1.notifySettingsManager()
    print(settings_manager._smap)
