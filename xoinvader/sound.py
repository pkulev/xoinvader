"""Sound files handling."""


import pygame

from xoinvader.common import Settings


pygame.mixer.init()


class _Mixer(object):
    """Handle sound files."""

    def __init__(self):
        self._sounds = dict()
        self._mute = True  # Settings.system.no_sound

    def register(self, object_id, sound_path):
        """Map object classname to sound object."""
        sound = pygame.mixer.Sound(sound_path)
        self._sounds.update({object_id: sound})

    def play(self, object_id, *args, **kwargs):
        """Play sound object."""
        if self._mute:
            return

        if object_id in self._sounds:
            self._sounds[object_id].play(*args, **kwargs)

    def mute(self):
        self._mute = True

    def unmute(self):
        self._mute = False

Mixer = _Mixer()
