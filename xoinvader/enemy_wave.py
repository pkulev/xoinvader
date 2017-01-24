"""Module for creating and maintaining waves of incoming enemies."""

class EnemyWave(object):
    """Container for enemy wave behavior.

    Intended to use as just container, but may be subclassed. It's useful in
    order to add methods for creating concrete animations and spawning actual
    enemies.

    :param int speed: relative speed of the wave. Means how fast time advances.
    The faster time advances, the shorter the delays between enemy spawns.
    :param dict events: map from relative time in event to function that spawns
    the enemies.
    :param bool running: if wave currently advances.
    """

    def __init__(self, speed=0):
        self._running = False
        self._counter = 0
        self._speed = speed
        self._events = {}
        self._event_timeouts = []

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def running(self):
        return self._running

    def add_event(self, time, callback):
        """Add spawning event to some point in time.

        :param int time: point in time relative to wave start when to run
        `callback`. Callback is fired when `_counter` exceeds provided value
        :param function callback: callback to be runned when wave reaches `time`
        """
        self._events.setdefault(time, []).append(callback)

    def start(self):
        """Start the enemy wave.

        Resets the counter, recomputes the list of event timeouts and sets the
        `running` property to `True`.
        """

        self._running = True
        self._counter = 0
        self._event_timeouts = sorted(self._events)

    def update(self):
        """Update the counter and fire appropriate events.

        Function is doing anything useful only when the EnemyWave has been
        started earlier, i.e. currently in running state.
        Function updates current timer and fires all events, which timeouts have
        expired. If there's no more events in the queue, the running state
        terminates and object goes to sleep.
        Time counter is increased by `_speed` value at each call of the
        fucntion.
        """

        if not self._running:
            return

        self._counter += self._speed
        while self._event_timeouts[0] <= self._counter:
            current_timeout = self._event_timeouts[0]
            for callback in self._events[current_timeout]:
                callback()
            del self._event_timeouts[0]
            if not self._event_timeouts:
                self._running = False
                break
