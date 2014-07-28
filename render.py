class Renderer(object):
    def __init__(self):
        self.__objects = []


    def add_object(self, obj):
        self.__objects.append(obj)


    def remove_object(self, obj):
        self.__objects.remove(obj)


    def render_all(self, screen):
        for obj in self.__objects:
            glob_pos, data_gen = obj.get_render_data()
            for el in data_gen:
                pos, image, style = el
                screen.addch(glob_pos.y + pos.y, glob_pos.x + pos.x, image)
