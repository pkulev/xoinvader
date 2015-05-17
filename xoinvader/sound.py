""" Sound files handling. """

import pygame

from xoinvader.common import Settings


pygame.mixer.init()


class _Mixer(object):
    """ Handle sound files. """

    def __init__(self):
        self._sounds = dict()

    def register(self, classname):
        """ Map object classname to sound object. """
        sound = pygame.mixer.Sound(Settings.path.sound.weapon[classname])
        self._sounds.update({classname: sound})

    def play(self, classname):
        """ Play sound object. """
        if classname in self._sounds:
            self._sounds[classname].play()


Mixer = _Mixer()
