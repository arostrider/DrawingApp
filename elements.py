from states import States
import util
import tkinter as tk


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
    HEIGHT = 8

    def __init__(self, _id, canvas, parent, start_x, start_y, direction, length):
        Element.__init__(self, _id, canvas, parent, start_x, start_y)
        self.start_x, self.start_y = start_x, start_y
        self.end_x, self.end_y = util.calc_vector_end_point(self.start_x, self.start_y, direction, length)

        self.image = self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y,
                                             width=self.HEIGHT, fill='red')
        self.bind_keys()

        print(f'Length({length}), Direction({direction})')


class Zglob(Element):
    RADIUS = Greda.HEIGHT / 2

    def __init__(self, _id, canvas, parent, origin_x, origin_y, radius=RADIUS):
        Element.__init__(self, _id, canvas, parent, start_x=origin_x, start_y=origin_y)
        self.image = self.canvas.create_circle(origin_x, origin_y, radius, fill="blue", width=2)
        self.bind_keys()

        # this does not do anything yet, but please check if removing
        self.radius = int(radius)


class Sila(Element):
    def __init__(self, _id, canvas, parent, attack_x, attack_y, attack_angle, intensity):
        Element.__init__(self, _id, canvas, parent, attack_x, attack_y)
        self.start_x, self.start_y = attack_x, attack_y
        self.end_x, self.end_y = util.calc_vector_end_point(self.start_x, self.start_y, attack_angle, intensity)

        self.image = self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y,
                                             width=4, fill='green', arrow=tk.FIRST)
        self.bind_keys()

        print(f'Intensity({intensity}), Attack angle({attack_angle})')
