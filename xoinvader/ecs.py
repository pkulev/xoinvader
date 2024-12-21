import uuid


# pylint: disable=all
class Entity:
    Catalog = {}
    __slots__ = ("name", "uid", "components")

    def __new__(cls, name, uid=None):
        if name not in cls.Catalog:
            entity = super().__new(cls)
            cls.Catalog[name] = entity
        else:
            entity = cls.Catalog[name]
        return entity

    def __hash__(self):
        return hash(self.uid)

    def __init__(self, name="", uid=None) -> None:
        self.name = name
        self.uid = uid or uuid.uuid4()
        self.components = {}

    def __repr__(self) -> str:
        cname = self.__class__.__name__
        name = self.name or self.uid
        if name != self.uid:
            name = f"{name}:{self.uid}"
        return f"<{cname} {name}>"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.uid == other.uid
        elif isinstance(other, self.uid.__class):
            return self.uid == other
        return False

    def __str__(self) -> str:
        return str(self.components)

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, val) -> None:
        if isinstance(val, Component):
            self.components[key] = val


class Component:
    pass


class System:
    pass
