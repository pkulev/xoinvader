"""Animation.

Animation is set of keyframes.
Value of selected attribute changes in time.

Keyframe:
  (time, value)

Objects have animation manager which manages animation graph and switching."""

from collections.abc import Iterable
from operator import itemgetter

from eaf import Timer

from xoinvader.utils import Point


class AnimationBoundariesExceeded(Exception):
    """Exception to show that interpolated value will be incorrect."""

    def __init__(self, first, current_time, second) -> None:
        super().__init__(
            self,
            f"Animation frame boundaries exceeded: {first} <= {current_time} <= {second}",
        )


class InterpolationUnknownTypes(Exception):
    """Such type combination is unsupported."""

    def __init__(self, first, second) -> None:
        super().__init__(
            self, f"Unknown types of interpolating values: {first} and {second}"
        )


# TODO: Implement animation graph and etc
class AnimationManager:
    """Manage list of object animation."""

    def __init__(self) -> None:
        self._animations = {}
        self._animation = None

    @property
    def animation(self) -> str:
        """AnimationManager's current animation name.

        To set animation - assign it's name.

        :getter: yes
        :setter: yes
        :type: str
        """

        if self._animation:
            return self._animation.name
        else:
            raise AttributeError("There is no available animation.")

    @animation.setter
    def animation(self, name: str) -> None:
        if name in self._animations:
            self._animation = self._animations[name]
        else:
            raise ValueError(f"No such animation: '{name}'.")

    def add(self, name: str, *args, **kwargs) -> None:
        """Add new animation, pass args to Animation class.

        See interface of `class::xoinvader.animation.Animation`.

        :param str name: animation name
        """

        animation = Animation(name, *args, **kwargs)
        self._animations[name] = animation

        if not self._animation:
            self._animation = animation

    def update(self, dt: int) -> None:
        """Update manager's state."""

        if not self._animation:
            return

        try:
            self._animation.update(dt)
        except StopIteration:
            return  # TODO: think about method to change animation


class Animation:
    """Animation unit.

    Animation object holds sorted list of (time, value) items and changes
    selected attribute of bound object according to local animation time.
    Time measured by timer. When current time is greater or equal then time
    of next keyframe - animation object changes it to appropriate value.
    When animation is done and if not looped - raise StopIteration.
    In case of interpolated animation value calculation occurs within two
    bounding frames and on frame switch.

    :param str name: animation name
    :param object bind: object to bind animation
    :param str attr: attribute to change in frames
    :param list keyframes: (float, object) tuples
    :param bool interp: interpolate values between frames or not
    :param bool loop: loop animation or not
    """

    def __init__(
        self,
        name: str,
        bind: object,
        attr: str,
        keyframes: list[tuple[float, object]],
        interp: bool = False,
        loop: bool = False,
    ) -> None:
        self._name = name
        self._obj = bind
        self._attr = attr

        if not keyframes:
            raise ValueError("Animation keyframes must not be empty.")
        self._keyframes = sorted(keyframes, key=itemgetter(0))

        self._interp = interp
        self._loop = loop

        # Timer for tracking local time
        self._timer = Timer(self._keyframes[-1][0], lambda: True)
        self._timer.start()

        # Current keyframe index
        self._current = 0

        if self._interp:
            self.update = self._update_interpolated
        else:
            self.update = self._update_discrete

    @property
    def name(self) -> str:
        """Animation's name."""
        return self._name

    def _apply_value(self, value: object) -> None:
        """Apply new value to linked object.

        :param value: value to apply
        """

        setattr(self._obj, self._attr, value)

    def _update_interpolated(self, dt: int) -> None:
        """Advance animation and interpolate value.

        .. important::

           Animation frame switching depends on interp mode animation with interpolation
           switches frame only when current local time exceeds NEXT frames' time border.
        """

        self._check_animation_state()
        self._timer.update(dt)

        current_time = self._timer.elapsed
        keyframe = self._keyframes[self._current]
        next_keyframe = self._keyframes[self._current + 1]

        # it's time to switch keyframe
        if current_time >= next_keyframe[0]:
            self._current += 1
            keyframe = self._keyframes[self._current]

        if self._current == len(self._keyframes) - 1:
            self._apply_value(keyframe[1])
            self._current += 1
            self._check_animation_state()
            return

        next_keyframe = self._keyframes[self._current + 1]

        value = interpolate(keyframe, next_keyframe, current_time)
        self._apply_value(value)

    def _update_discrete(self, dt: int) -> None:
        """Advance animation without interpolating value.

        .. important::

           Animation frame switching depends on interp mode discrete animation swiches frame and
           updates value only if current local time is >= time of current keyframe.

           No need to worry about calculating value between frames - thus no need to complicate
           behaviour.
        """

        self._check_animation_state()
        self._timer.update(dt)

        keyframe = self._keyframes[self._current]

        # Check if animation need to switch keyframe
        if self._timer.elapsed >= keyframe[0]:
            self._apply_value(keyframe[1])
            self._current += 1

    def _check_animation_state(self) -> None:
        """Check animation state and restart if needed.

        :raise StopIteration: when animation exceeded frames.
        """

        if len(self._keyframes) == self._current:
            if self._loop:
                self._current = 0
                self._timer.restart()
            else:
                self._timer.stop()
                raise StopIteration


def linear_equation(
    val1: float,
    val2: float,
    time1: float,
    time2: float,
    current_time: float,
) -> float:
    """Linear equation to get interpolated value.

    :param val1: first keyframe value
    :param val2: second keyframe value
    :param time1: first keyframe local time
    :param time2: second keyframe local time
    :param current_time: current animation local time
    """

    return val1 + (val2 - val1) / (time2 - time1) * (current_time - time1)


def same_type(values: Iterable[object], types: type | tuple[type]) -> bool:
    """Check if values are belongs to same type or type tuple.

    :param values: values to check type similarity
    :param types: type or tuple of types
    """

    return all(map(lambda it: isinstance(it, types), values))


def interpolate(first, second, current_time):
    """Interpolate value by two bounding keyframes.

    :param collections.Iterable first: first bounding keyframe
    :param collections.Iterable second: second bounding keyframe
    :param float current_time: current animation local time

    :raises AnimationBoundariesExceeded: when time interval is invalid
    :raises InterpolationUnknownTypes: when interpolating invalid types
    """

    if not first[0] <= current_time <= second[0]:
        raise AnimationBoundariesExceeded(first[0], current_time, second[0])

    def frames_of(*args: type) -> None:
        """Return whether frames both of specified type."""

        return same_type((first[1], second[1]), args)

    if frames_of(int, float):
        value = linear_equation(
            float(first[1]),
            float(second[1]),
            float(first[0]),
            float(second[0]),
            float(current_time),
        )

    elif frames_of(Point):
        value = linear_equation(
            first[1],  # TODO FIXME: check, it seems that this case is broken
            second[1],
            float(first[0]),
            float(second[0]),
            float(current_time),
        )
    else:
        raise InterpolationUnknownTypes(type(first[1]), type(second[1]))

    return value
