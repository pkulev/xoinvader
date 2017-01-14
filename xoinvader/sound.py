"""Sound files handling."""


from xoinvader.common import Settings
from xoinvader.utils import Singleton


def get_mixer():
    """Returns appropriate mixer class.

    :return: mixer implementation
    :rtype: class
    """

    choises = {
        True: DummyMixer,
        False: PygameMixer
    }

    return choises[Settings.system.no_sound]


class DummyMixer(object):
    """Mixer stub for no-sound mode."""

    def __init__(self):
        pass

    def register(self, *args, **kwargs):
        """Dummy register."""
        pass  # TODO: logging: [sound::DummyMixer] Registering ...

    def play(self, *args, **kwargs):
        """Dummy play."""
        pass

    def mute(self):
        """Dummy mute."""
        pass

    def unmute(self):
        """Dummy unmute."""
        pass


class PygameMixer(object, metaclass=Singleton):
    """Handle sound files."""

    def __init__(self):
        # TODO: make 'sound' package alike 'application'
        # TODO: import appropriate sound class from separate files
        import pygame
        self.pygame = pygame  # Do not try it home

        self.pygame.mixer.init()

        self._sounds = dict()
        self._mute = Settings.system.no_sound

    def register(self, object_id, sound_path):
        """Map object classname to sound object."""
        sound = self.pygame.mixer.Sound(sound_path)
        self._sounds.update({object_id: sound})

    def play(self, object_id, *args, **kwargs):
        """Play sound object."""
        if self._mute:
            return

        if object_id in self._sounds:
            self._sounds[object_id].play(*args, **kwargs)

    def mute(self):
        """Mute."""
        self._mute = True

    def unmute(self):
        """Unmute."""
        self._mute = False


Mixer = get_mixer()  # pylint: disable=invalid-name
