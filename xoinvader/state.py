"""Provides basic game state classes."""

import logging
from typing import (
    Sequence,
    Union,
)

from xoinvader import render


LOG = logging.getLogger(__name__)


class State:
    """Base class for game states.

    State is a container for game objects (instances of GameObject), objects
    are belong to the state. User should add and remove objects via state
    methods. Other systems (e.g. collision or animation) must carefully refer
    to state objects to not cause memory leaks.

    .. warning:: implement actor base class

    :param owner: state's owner
    :type owner: `xoinvader.application.Application`
    """

    def __init__(self, owner):
        LOG.info("Instantiating %s state.", self.__class__.__name__)

        self._owner = owner
        self._actor = None
        self._screen = None

        self._objects = []

    def postinit(self):
        """Do all instantiations that require prepared State object."""

        LOG.debug("Post init %s state.", self.__class__.__name__)

    def trigger(self, *args, **kwargs):
        """Common way to get useful information for triggered state."""

        LOG.debug("Triggering %s state with %s and %s",
                  self.__class__.__name__, args, kwargs)

    @property
    def owner(self):
        """State's owner.

        :getter: yes
        :setter: no
        :type: :class:`xoinvader.application.Application`
        """
        return self._owner

    @property
    def actor(self):
        """Controllable object.

        :getter: yes
        :setter: no
        :type: object
        """
        return self._actor

    @property
    def screen(self):
        """Screen for rendering state's objects.

        :getter: yes
        :setter: no
        :type: `curses.Window`
        """
        return self._screen

    def events(self):
        "Event handler, called by `Application.loop` method."
        raise NotImplementedError

    def update(self):
        """Update handler, called every frame."""

        for obj in self._objects:
            obj.update()

    def render(self):
        """Render handler, called every frame."""

        self._screen.erase()
        self._screen.border(0)

        # TODO: abstract renderer or move it to application
        render.render_objects(self._objects, self._screen)
        self._screen.refresh()


    # TODO: [object-system]
    #  * implement GameObject common class for using in states
    #  * generalize interaction with game objects and move `add` to base class
    # ATTENTION: renderables that added by another objects in runtime will not
    #  render at the screen, because they must register in state via this func
    #  as others. This is temporary decision as attempt to create playable game
    #  due to deadline.
    def add(self, obj: Union[object, Sequence[object]]):
        """Add GameObject to State's list of objects.

        State will call GameObject.update() and pass to render all it's objects
        every frame.
        """

        obj = obj if isinstance(obj, (list, tuple)) else [obj]
        self._objects += obj
        LOG.debug("%s", obj)

        # TODO: Because we don't have common GameObject interface
        # This is temporary smellcode
        for item in obj:
            if item.compound:
                subitems = item.get_renderable_objects()
                LOG.debug("Subitems: %s", subitems)
                self._objects += subitems

    def remove(self, obj: object):
        """Remove GameObject from State's list of objects.

        Removed objects should be collected by GC.
        """

        LOG.debug("%s", obj)

        try:
            if obj.compound:
                for subobj in obj.get_renderable_objects():
                    self._objects.remove(subobj)
                    del subobj
            self._objects.remove(obj)
        except ValueError:
            LOG.exception("Object %s is not in State's object list.", obj)
        finally:
            del obj
