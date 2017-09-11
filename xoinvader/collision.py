"""Collision detection system and component module."""

import functools
import logging
import weakref

from xoinvader import application
from xoinvader.utils import Point


LOG = logging.getLogger(__name__)


COLLISIONS = {}
"""Global mapping TypePair <=> [callable]."""


class CollisionManagerNotFound(Exception):
    """Raises on try to register collider without instantiated manager."""

    def __init__(self):
        super(CollisionManagerNotFound, self).__init__(
            "You can't use Collider objects without "
            "CollisionManager. Please create it first.")


class TypePair(object):
    """Class for hashable ordered string pairs.

    Used as collision dictionary keys, containing pair of collider types.
    Not commutative, TypePair(a, b) != TypePair(b, a)
    It's needed to store and get exact handler as it was registered.

    :param str first: first collider type
    :param str second: second collider type
    """

    def __init__(self, first, second):
        self._first = first
        self._second = second
        self._pair = first + '_' + second

    @property
    def first(self):
        """First collider type.

        :getter: yes
        :setter: no
        :type: type
        """
        return self._first

    @property
    def second(self):
        """Second collider type.

        :getter: yes
        :setter: no
        :type: type
        """
        return self._second

    def __eq__(self, other):
        return self._pair == other._pair  # pylint: disable=protected-access

    def __hash__(self):
        return hash(self._pair)

    def __str__(self):
        return "TypePair({0}, {1})".format(self._first, self._second)


def register(left, right):
    """Collision handler registration decorator.

    .. Note:: Argument order matters! Handler must belong to first object.

    :param str left: first collidable object
    :param str right: right collidable object
    """

    def decorator(handler):
        COLLISIONS.setdefault(TypePair(left, right), []).append(handler)

        @functools.wraps(handler)
        def handle(*args, **kwargs):
            return handler(*args, **kwargs)

        return handle

    return decorator


class CollisionManager(object):
    """Class for collision detection between known components.

    To process collisions, first update the positions of all objects of
    interest, then call `update` method. It will traverse all registered
    collisions (between pairs of types) and call appropriate handlers in order
    they were registered for the two types of colliding objects.

    If you just want to check, if two Colliders collide, call `check_collision`
    on them.
    """

    # Marker of solid matter inside collider physics map
    __solid_matter__ = "#"

    def __init__(self):
        self._colliders = weakref.WeakSet()
        self._collisions = COLLISIONS

    def add(self, collider):
        """Add collider.

        :param :class:`xoinvader.collision.Collider` collider:
        """

        LOG.debug("Adding collider %s\n pos: %s", collider, collider.pos)
        self._colliders.add(collider)

    def remove(self, collider):
        """Remove collider.

        :param :class:`xoinvader.collision.Collider` collider:
        """

        LOG.debug("Removing collider %s\n pos %s", collider, collider.pos)
        self._colliders.remove(collider)

    # pylint: disable=too-many-nested-blocks
    def update(self):
        """Detect and process all collisions."""

        for pair in self._collisions:
            colliders_type_1 = [
                item for item in self._colliders
                if item.col_type == pair.first]
            colliders_type_2 = [
                item for item in self._colliders
                if item.col_type == pair.second]
            for collider_1 in colliders_type_1:
                for collider_2 in colliders_type_2:
                    collision_rect = self.check_collision(
                        collider_1, collider_2)
                    if collision_rect:
                        for callback in self._collisions[pair]:
                            callback(collider_1.obj, collider_2.obj,
                                     collision_rect)

    # pylint: disable=too-many-locals
    @staticmethod
    def check_collision(col_1, col_2):
        """Check collisions between two colliders.

        Returns `None` if no collision occured, or returns rectangle of
        overlapping region between collider maps.

        :param col1: first collider
        :type col1: :class:`Collider`
        :param col2: second collider
        :type col2: :class:`Collider`
        :rtype: tuple of two :class:`Point`
        """

        width_1 = max(map(len, col_1.phys_map))
        height_1 = len(col_1.phys_map)
        topleft_1 = col_1.pos
        botright_1 = topleft_1 + Point(width_1, height_1)

        width_2 = max(map(len, col_2.phys_map))
        height_2 = len(col_2.phys_map)
        topleft_2 = col_2.pos
        botright_2 = topleft_2 + Point(width_2, height_2)
        if (
                topleft_1.x >= botright_2.x or topleft_1.y >= botright_2.y or
                botright_1.x <= topleft_2.x or botright_1.y <= topleft_2.y
        ):
            # Definelty not overlapping
            return
        # Now find where exactopleft_y overlapping occured
        topleft_overlap = Point(
            max(topleft_1.x, topleft_2.x),
            max(topleft_1.y, topleft_2.y))
        botright_overlap = Point(
            min(botright_1.x, botright_2.x),
            min(botright_1.y, botright_2.y))
        # Now find if they actually collided
        # first, calculate offsets
        overlap_1 = Point()
        overlap_2 = Point()
        overlap_1.x = abs(topleft_1.x - topleft_overlap.x)
        overlap_1.y = abs(topleft_1.y - topleft_overlap.y)
        overlap_2.x = abs(topleft_2.x - topleft_overlap.x)
        overlap_2.y = abs(topleft_2.y - topleft_overlap.y)
        # iterate over overlapping region
        # and search for collision
        for i in range(botright_overlap.x - topleft_overlap.x):
            for j in range(botright_overlap.y - topleft_overlap.y):
                # TODO: check length of current y-level string
                # it might be not enough to contain i + ox1/2 element
                if (
                        col_1.phys_map[j + overlap_1.y][i + overlap_1.x] ==
                        col_2.phys_map[j + overlap_2.y][i + overlap_2.x] ==
                        CollisionManager.__solid_matter__
                ):
                    return (topleft_overlap, botright_overlap)


class Collider(object):
    """Collider component class.

    When added to object, enables it to participate in coliision processing
    system: i.e. to be able to detect and process collisions between the object
    and other ones.

    .. Attention:: CollisionManager must be created first and must be
                   accessible via State.

    :param object obj: GameObject to which the collider is linked
    :param list phys_map: list of strings representing collider physical
    geometry. All strings must be of equal length. Class member
    __solid_matter__ of CollisionManager represents solid geometry, all other
    chars are treated as void space and may be any.
    """

    def __init__(self, obj, phys_map):
        self._obj = obj
        self._col_type = self._obj.type()
        self._phys_map = phys_map

        # TODO: move collision to State.systems
        try:
            application.get_current().state.collision.add(self)
        except AttributeError:
            raise CollisionManagerNotFound()

    @property
    def phys_map(self):
        """Collider physical geometry.

        :getter: yes
        :setter: no
        :type: list
        """
        return self._phys_map

    @property
    def col_type(self):
        """Collider type name.

        :getter: yes
        :setter: no
        :type: str
        """
        return self._col_type

    @property
    def pos(self):
        """Collider's left top position.

        :getter: yes
        :setter: no
        :type: :class:`Point`
        """
        return self._obj.pos[int]

    @property
    def obj(self):
        return self._obj
