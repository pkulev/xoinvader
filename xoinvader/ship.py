"""Enemy and player ships."""


from xoinvader.sound import Mixer
from xoinvader.render import Renderable
from xoinvader.weapon import Blaster, Laser, UM, EBlaster
from xoinvader.utils import Point, Surface, InfiniteList
from xoinvader.common import Settings, get_json_config


CONFIG = get_json_config(Settings.path.config.ships)


class Ship(Renderable):
    """Base class for all ships. Contains basic ship logic."""

    def __init__(self, pos, border, settings):
        self._type = self.__class__.__name__
        self._image = None

        self._pos      = pos
        self._border   = border
        self._settings = settings

        self._dx      = None
        self._fire    = False
        self._weapon  = None
        self._weapons = InfiniteList()
        self._wbay = None
        self._direction = 0

        self._max_hull   = None
        self._max_shield = None
        self._hull       = None
        self._shield     = None

        # first initialization
        self._load_config(CONFIG[self.__class__.__name__])

    def _load_config(self, config):
        """Load config from mapping."""
        if not config:
            raise ValueError

        self._dx         = int(config.dx)
        self._hull       = int(config.hull)
        self._shield     = int(config.shield)
        self._max_hull   = int(config.max_hull)
        self._max_shield = int(config.max_shield)

    @property
    def max_hull(self):
        return self._max_hull

    @property
    def max_shield(self):
        return self._max_shield

    def getHullPercentage(self):
        """Return hull percentage."""
        return self._hull * 100.0 / self._max_hull

    def getShieldPercentage(self):
        """Return shield percentage."""
        return self._shield * 100.0 / self._max_shield

    def getWeaponPercentage(self):
        """Return weapon load percentage."""
        return self._weapon.loadPercentage()

    def get_render_data(self):
        """Callback for rendering."""
        return [self._pos], self._image.get_image()

    def get_renderable_objects(self):
        """CORP stub."""
        return self._weapons

    def move_left(self):
        """Change direction."""
        self._direction = -1

    def move_right(self):
        """Change direction."""
        self._direction = 1

    def toggle_fire(self):
        """Toggle current weapon fire mode."""
        self._fire = not self._fire

    def next_weapon(self):
        """Select next weapon."""
        self._weapon = self._weapons.next()

    def prev_weapon(self):
        """Select previous weapon."""
        self._weapon = self._weapons.prev()

    def add_weapon(self, weapon):
        """Add new weapon."""
        self._weapons.append(weapon)
        self._weapon = weapon
        self._settings.renderer.add_object(self._weapon)

    def update(self):
        """Update ship object's state."""

        # TODO:
        # think about those who has dx > 1
        if self._pos.x == self._border.x - self._image.width - 1 and self._dx > 0:
            self._pos.x = 0
        elif self._pos.x == 1 and self._dx < 0:
            self._pos.x = self._border.x - self._image.width

        self._pos.x += self._direction * self._dx
        self._direction = 0

        for weapon in self._weapons:
            weapon.update()

        if self._fire:
            try:
                self._weapon.make_shot(Point(x=self._pos.x + self._wbay.x,
                                             y=self._pos.y + self._wbay.y))
            except ValueError:
                self.next_weapon()

        self.refresh_shield()

    def take_damage(self, damage):
        """Calculate and apply damage to shield and hull."""
        if self._shield < damage:
            rest_damage = damage - self._shield
            self._shield = 0
            self._hull -= rest_damage
        else:
            self._shield -= damage
        if self._hull < 0:
            self._hull = 0

    def refresh_shield(self, amount=1):
        """Refresh shield."""
        if self._shield == self._max_shield:
            return

        if self._shield + amount > self._max_shield:
            self._shield = self._max_shield
        else:
            self._shield += amount


class GenericXEnemy(Ship):
    """Generic X enemy class."""

    def __init__(self, pos, border, settings):
        super(GenericXEnemy, self).__init__(pos, border, settings)
        self._image = Surface([[' ', '*', ' '],
                               [' ', 'X', ' '],
                               ['x', '^', 'x']],
                              reverse=True)

        self.add_weapon(EBlaster())
        self._settings.renderer.add_object(self._weapon)
        self._fire = True
        self._wbay = Point(x=self._image.width // 2, y=1)


class Playership(Ship):
    """Playership class. Contains additional methods for HUD."""

    def __init__(self, pos, border, settings):
        super(Playership, self).__init__(pos, border, settings)

        self._image = Surface([[' ', ' ', 'O', ' ', ' '],
                               ['<', '=', 'H', '=', '>'],
                               [' ', '*', ' ', '*', ' ']])

        self._pos = Point(x=pos.x - self._image.width // 2,
                          y=pos.y - self._image.height)
        self._border = border
        self._settings = settings

        self._fire = False
        self._weapons = InfiniteList([Blaster(), Laser(), UM()])
        for weapon in self._weapons:
            self._settings.renderer.add_object(weapon)

        self._weapon = self._weapons.current()
        self._wbay = Point(x=self._image.width // 2, y=-1)

        Mixer.register(".".join([self._type, "engine"]),
                       Settings.path.sound.ship[self._type].engine)

    def get_weapon_info(self):
        """Return information about current weapon."""
        return "Weapon: {w} | [{c}/{m}]".format(w=self._weapon.type,
                                                c=self._weapon.ammo,
                                                m=self._weapon.max_ammo)
