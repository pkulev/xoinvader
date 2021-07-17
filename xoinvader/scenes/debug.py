"""Scene for debug and introspection."""

from xoinvader.keys import KEY
from xoinvader.handlers import EventHandler
from xoinvader import app

from eaf import State
from xo1 import Renderable, Surface


class TestColors(Renderable):
    def __init__(self, pos):
        super().__init__(pos)

        self._image = None

    def update(self, dt):
        pass


class DebugState(State):
    def postinit(self):
        from xoinvader.ship import PlayerShip
        from xoinvader.gui import TextWidget
        from xoinvader.collision import CollisionManager
        from xoinvader import app

        DebugState.collision = CollisionManager()

        from eaf import Vec3

        self._events = EventHandler(
            self,
            {
                KEY.ESCAPE: lambda: app.current().trigger_state(
                    "PauseMenuState"
                ),
            },
        )

        self.actor = PlayerShip(Vec3())
        self.add(self.actor)
        self.add(
            TextWidget(Vec3(10, 10), str(self.actor.image.image[0][2].attr))
        )
        self.add(TestColors(Vec3(20, 20)))

    def events(self):
        self._events.handle()

    def find_by_class(self, state, classname):
        o = []
        for obj in app.current().states[classname].objects:
            if isinstance(obj, classname):
                o.append(obj)

        return o
