from states import States


class Element:

    def __init__(self, _id, canvas, parent_main_class):
        self.id = _id
        self.canvas = canvas
        self.parent = parent_main_class
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
        Element.__init__(self, _id, canvas, parent)
        self.image = self.canvas.create_line(start_x, start_y, end_x, end_y, **kwargs)
        self.bind_keys()

        # this does not do anything yet, but please check if removing
        self.start_x = int(start_x)
        self.start_y = int(start_y)
        self.end_x = int(end_x)
        self.end_y = int(end_y)


class Circle(Element):
    def __init__(self, _id, canvas, parent, origin_x, origin_y, radius, **kwargs):
        Element.__init__(self, _id, canvas, parent)
        self.image = self.canvas.create_circle(origin_x, origin_y, radius, **kwargs)
        self.bind_keys()

        # this does not do anything yet, but please check if removing
        self.origin_x = int(origin_x)
        self.origin_y = int(origin_y)
        self.radius = int(radius)
