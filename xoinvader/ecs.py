import uuid


#pylint: disable=all
class Entity(object):
    Catalog = {}
    __slots__ = ("name", "uid", "components")

    def __new__(cls, name, uid=None):
        if name not in cls.Catalog:
            entity = super(Entity, cls).__new(cls)
            cls.Catalog[name] = entity
        else:
            entity = cls.Catalog[name]
        return entity

    def __hash__(self):
        return hash(self.uid)

    def __init__(self, name="", uid=None):
        self.name = name
        self.uid = uid or uuid.uuid4()
        self.components = {}

    def __repr__(self):
        cname = self.__class__.__name__
        name = self.name or self.uid
        if name != self.uid:
            name = "{0}:{1}".format(name, self.uid)
        return "<{0} {1}>".format(cname, name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.uid == other.uid
        elif isinstance(other, self.uid.__class):
            return self.uid == other
        return False

    def __str__(self):
        return str(self.components)

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, val):
        if isinstance(val, Component):
            self.components[key] = val


class Component(object):
    pass


class System(object):
    pass
