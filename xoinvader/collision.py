"""Collision detection system and component module."""

import weakref

from xoinvader.utils import Point


class TypePair(object):
    """Class for hashable unordered string pairs.

    Used as collision dictionary keys, containing pair of collider types. It's
    set-like, i.e. TypePair(a, b) == TypePair(b, a) and their hashes are equal
    too.

    :param str first: first collider type
    :param str second: second collider type
    """

    def __init__(self, first, second):
        first, second = sorted([first, second])
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
        if Collider.__manager__ is None:
            def null_manager(_):
                """Manager nuller."""
                Collider.__manager__ = None

            Collider.__manager__ = weakref.ref(self, null_manager)
        self._colliders = []
        self._collisions = {}

    def _add(self, collider):
        """Add collider."""
        self._colliders.append(collider)

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
                            if callback:
                                callback(collision_rect)

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

    def _add_collision(self, collider, other_classname, callback=None):
        """Add collision handler.

        Adds handler to be called when collision of colliders of `col_type`
        `other_classname` and `collider`'s `col_type` occurs.

        :param collider: collider to which type's add handler
        :type collider: :class:`Collider`
        :param str other_classname: type name of other collider instances to
        check collisions with
        :paran function callback: handler callback. Function that is called
        whenever collision is detected
        """

        if collider not in self._colliders:
            raise ValueError(
                "Attempt to add collision handler for "
                "unregistered collider {0}".format(collider))
        type_pair = TypePair(collider.col_type, other_classname)
        self._collisions.setdefault(type_pair, []).append(callback)


class Collider(object):
    """Collider component class.

    When added to object, enables it to participate in coliision processing
    system: i.e. to be able to detect and process collisions between the object
    and other ones.

    :param str col_type: name of the collider type. Used in processing possible
    collisions
    :param list phys_map: list of strings representing collider physical
    geometry. All strings must be of equal length. Class member
    __solid_matter__ of CollisionManager represents solid geometry, all other
    chars are treated as void space and may be any.
    :param pos: left top corner of collider map
    :type pos: :class:`Point`
    """

    __manager__ = None

    def __init__(self, col_type, phys_map, pos):
        if Collider.__manager__ is None:
            raise ValueError(
                "You can't use Collider objects without "
                "ColliderManager. Please create it first.")
        self._mgr = Collider.__manager__()  # manager is weakreaf, thus '()'
        self._col_type = col_type
        self._pos = pos
        self._phys_map = phys_map
        self._mgr._add(self)  # pylint: disable=protected-access

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
        return self._pos

    def add_handler(self, other_type, callback=None):
        """Install handler for collision with type `other_type`.

        Handler is fired when collision between current collider and any other
        collider of type `other_type` detected by `update` method of class
        :class:`CollisionManager`. Callback is `None` by default.

        :param str other_type: type of collider to install collision handler
        with
        :param function callback: function which is called when current
        CollisionManager's update method detects collision of this collider
        with collider of type `other_type`
        """

        # pylint: disable=protected-access
        self._mgr._add_collision(self, other_type, callback)
