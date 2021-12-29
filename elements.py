from states import States

class Element:

    def __init__(self, _id, canvas, parent_main_class):
        self.id = _id
        self.canvas = canvas
        self.parent = parent_main_class
        print(f'Created: {self} with ID: {self.id}')

    def mouse_click_on_element(self):
        print(f'Click on: {self}')
        if self.parent.state == States.CLEAR:
            self.parent.selected_element = self
            print(f'Element with ID {self.parent.selected_element.id} is now selected')
        return self


class Line(Element):
    def __init__(self, _id, canvas, parent, start_x, start_y, end_x, end_y, **kwargs):
        Element.__init__(self, _id, canvas, parent)
        self.image = self.canvas.create_line(start_x, start_y, end_x, end_y, **kwargs)
        self.canvas.tag_bind(self.image, '<Button-1>', lambda event: self.mouse_click_on_element())


class Circle(Element):
    def __init__(self, _id, canvas, parent, origin_x, origin_y, radius, **kwargs):
        Element.__init__(self, _id, canvas, parent)
        self.image = self.canvas.create_circle(origin_x, origin_y, radius, **kwargs)
        self.canvas.tag_bind(self.image, '<Button-1>', lambda event: self.mouse_click_on_element())
