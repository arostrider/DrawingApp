from states import States
import util


class Element:

    def __init__(self, _id, canvas, parent_main_class, start_x, start_y):
        self.id = _id
        self.parent = parent_main_class
        self.canvas = canvas
        self.start_x = int(start_x)
        self.start_y = int(start_y)
        print(f'Created: {self} with ID: {self.id}')

    def bind_keys(self):
        self.canvas.tag_bind(self.image, '<Button-1>', lambda event: self.mouse_click_on_element())
        self.canvas.tag_bind(self.image, '<B1-Motion>', lambda event: self.mouse_drag_element())

    def mouse_click_on_element(self):
        print(f'Click on: {self}')
        if self.parent.state == States.CLEAR:
            self.parent.selected_element = self
            print(f'Element with ID {self.parent.selected_element.id} is now selected')
        return self

    def mouse_drag_element(self):
        self.parent.move_element(self.parent.selected_element, self.parent.mouse_x, self.parent.mouse_y)


class Line(Element):
    def __init__(self, _id, canvas, parent, start_x, start_y, end_x, end_y, **kwargs):
        Element.__init__(self, _id, canvas, parent, start_x, start_y)
        self.image = self.canvas.create_line(start_x, start_y, end_x, end_y, **kwargs)
        self.bind_keys()

        # this does not do anything yet, but please check if removing
        self.end_x = int(end_x)
        self.end_y = int(end_y)


class Circle(Element):
    def __init__(self, _id, canvas, parent, origin_x, origin_y, radius, **kwargs):
        Element.__init__(self, _id, canvas, parent, start_x=origin_x, start_y=origin_y)
        self.image = self.canvas.create_circle(origin_x, origin_y, radius, **kwargs)
        self.bind_keys()

        # this does not do anything yet, but please check if removing
        self.radius = int(radius)


class Greda(Element):
    HEIGHT = 4

    def __init__(self, _id, canvas, parent, start_x, start_y, length, direction, **kwargs):
        Element.__init__(self, _id, canvas, parent, start_x, start_y)
        # TODO: current implementation works only if angle is 45 degrees. implement properly
        self.a_x, self.a_y = start_x + self.HEIGHT * util.cos(direction), start_y - self.HEIGHT * util.sin(direction)
        self.d_x, self.d_y = start_x - self.HEIGHT * util.cos(direction), start_y + self.HEIGHT * util.sin(direction)

        self.end_x, self.end_y = util.calc_vector_end_point(start_x, start_y, angle=direction, length=length)
        self.b_x, self.b_y = self.end_x + self.HEIGHT * util.cos(direction), self.end_y - self.HEIGHT * util.sin(direction)
        self.c_x, self.c_y = self.end_x - self.HEIGHT * util.cos(direction), self.end_y + self.HEIGHT * util.sin(direction)

        self.point_coords = [self.a_x, self.a_y,
                             self.b_x, self.b_y,
                             self.c_x, self.c_y,
                             self.d_x, self.d_y]
        self.point_coords = [int(coord) for coord in self.point_coords]

        self.image = self.canvas.create_polygon(*self.point_coords, fill='red')
        self.bind_keys()

        print(f'Point coords: {self.point_coords}')
        print(f'Length({length}), Direction({direction})')
