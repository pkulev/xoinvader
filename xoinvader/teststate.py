import pygame
import pygame.locals

from pygame.locals import K_a, K_d, K_ESCAPE

from xoinvader.common import _ROOT

#from xoinvader.ship import TestShip
class TestShip():
    def __init__(self):
        self._image = pygame.image.load(_ROOT + "/res/gfx" + "/ship.png")

    def render(self):
        pass
    def move_left(self):
        print("MOVE: <LEFT>")
    def move_right(self):
        print("MOVE: <RIGHT>")
    def update(self):
        pass


from xoinvader.handlers import Handler
from xoinvader.state import State


class TestStateInputHandler(Handler):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)

        self._commands = {
            pygame.KEYDOWN: {
                K_a: self._actor.move_left,
                K_d: self._actor.move_right,
                K_ESCAPE: self._owner._owner.stop},
            pygame.KEYUP: {}}

    def handle(self, event):
        cmd = self._commands.get(event.type).get(event.key)
        if cmd:
            cmd()


class TestStateEventHandler(Handler):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)

        self._input_handler = TestStateInputHandler(owner)

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._owner.stop()
            elif event.type in [pygame.KEYUP, pygame.KEYDOWN]:
                self._input_handler.handle(event)
        # Some other event logic


class TestState(State):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        self._objects = []
        self._screen = self._owner.screen

        self._actor = TestShip()

        self._objects.append(self._actor)
        self._events = TestStateEventHandler(self)

    def events(self):
        self._events.handle()

    def update(self):
        for obj in self._objects:
            obj.update()

    def render(self):
        for obj in self._objects:
            obj.render()
