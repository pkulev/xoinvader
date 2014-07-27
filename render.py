

class Renderer(object):
    __created = False
    def __init__(self):
        if self.__class__.__created:
            raise Exception("Renderer already exists!")
        self.__objects = []
        self.__class__.__created = True

    def __del__(self):
        self.__class__.__created = False

    def add_object(self, obj):
        self.__objects.append(obj)

    def remove_object(self, obj):
        self.__objects.remove(obj)

    def render_all(self, screen):
        for obj in self.__objects:
            for image, pos in obj.get_render_data():
                screen.addch(pos.y, pos.x, image, obj.style)
