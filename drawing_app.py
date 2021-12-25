import sys
import util
from tkinter import *
import tkinter.font

from enum import Enum
from functools import wraps


def create_circle(self, x, y, r, **kwargs):
    """Custom, more intuitive method for drawing circle on tkinter.Canvas"""
    try:
        # TODO: reduce number of exceptions covered with this block
        x, y, r = int(x), int(y), int(r)
    except Exception as ex:
        print(ex)

    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


# adding a method to tkinter library
tkinter.Canvas.create_circle = create_circle


class States(Enum):
    CLEAR = 0
    WAIT_LINE_COORDINATES = 1
    WAIT_CIRCLE_COORDINATES = 2


class MouseStates(Enum):
    CLEAR = 0
    CLICKED = 1


# TODO: replace legacy gui widgets with tkinter.ttk widgets where possible
# TODO: organize widgets among frames
# TODO: setup grid as geometry manager instead of place

# TODO: think of splitting drawing line into two parts (start and end point coordinates input)


print("Hello World")


class MainWindow:
    def __init__(self, parent):
        self.gui(parent)
        self.bind_keys()

        self.mouse_x, self.mouse_y = 0, 0
        self.mouse_state = MouseStates.CLEAR

        self.state = States.CLEAR

        self.text_buffer = ""

    def gui(self, parent):
        # TODO: get rid of this If-else block
        if parent == 0:
            self.root = Tk()
            self.root.geometry('500x570')
        else:
            self.root = Frame(parent)
            self.root.place(x=0, y=0, width=500, height=570)

        # drawing canvas
        self.canvas = Canvas(self.root, bg='white')
        self.canvas.place(x=10, y=7, width=480, height=370)

        # output text box
        self.cmd_output = Text(self.root, bg="#000000", fg="#ffffff",
                               font=tkinter.font.Font(family="Consolas", size=10),
                               cursor="arrow", state="normal")
        self.cmd_output.place(x=10, y=380, width=480, height=120)

        # closing button
        self.button_close = Button(self.root, text="Close", font=tkinter.font.Font(family="MS Shell Dlg 2", size=8),
                                   cursor="arrow", state="normal")
        self.button_close.place(x=400, y=530, width=90, height=32)
        self.button_close['command'] = self.close_window

        # input text box
        self.input_var = StringVar()
        self.cmd_input = Entry(self.root, textvariable=self.input_var, bg="#242424", fg="#ffffff",
                               font=tkinter.font.Font(family="Consolas", size=10),
                               cursor="arrow", state="normal")
        self.cmd_input.place(x=60, y=500, width=430, height=22)

        # enter button
        self.button_enter = Button(self.root, text=">>>", font=tkinter.font.Font(family="Consolas", size=10),
                                   cursor="arrow",
                                   state="normal")
        self.button_enter.place(x=10, y=500, width=50, height=22)
        self.button_enter['command'] = self.cmd_enter

        # TODO: make label backgrounds transparent
        self.label_x_var = StringVar()
        self.label_x = Label(self.canvas, textvariable=self.label_x_var, fg="black", bg='white',
                             font=tkinter.font.Font(family="MS Shell Dlg 2", size=8), cursor="arrow", state="normal")
        self.label_x.place(x=395, y=345, width=35, height=22)

        self.label_y_var = StringVar()
        self.label_y = Label(self.canvas, textvariable=self.label_y_var, fg="black", bg='white',
                             font=tkinter.font.Font(family="MS Shell Dlg 2", size=8), cursor="arrow", state="normal")
        self.label_y.place(x=435, y=345, width=35, height=22)

    def bind_keys(self):
        self.cmd_input.bind('<Return>', lambda event: self.cmd_enter())
        self.canvas.bind('<Motion>', lambda event: self.mouse_over_canvas(event))
        self.canvas.bind('<Button-1>', lambda event: self.mouse_left_click_canvas(event))

    def close_window(self):
        self.root.destroy()
        print('window closed')
        sys.exit()

    def cmd_enter(self):
        text = self.cmd_input.get()
        self.do_action(text)
        self.cmd_input.delete(0, END)

    def set_mouse_coordinates(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y

    def mouse_over_canvas(self, event):
        self.set_mouse_coordinates(event)
        self.label_x_var.set(f"X: {self.mouse_x}")
        self.label_y_var.set(f"Y: {self.mouse_y}")

    def mouse_left_click_canvas(self, event):
        if self.state == States.CLEAR:
            pass

        elif self.state == States.WAIT_LINE_COORDINATES:
            self.draw_line_using_mouse_pointer(event)

        elif self.state == States.WAIT_CIRCLE_COORDINATES:
            self.draw_circle_using_mouse_pointer(event)

        print(self.mouse_state)

    def draw_line_using_mouse_pointer(self, event):
        self.set_mouse_coordinates(event)

        if self.mouse_state == MouseStates.CLEAR:
            self.text_buffer += f"{self.mouse_x} {self.mouse_y} "
            self.mouse_state = MouseStates.CLICKED

        elif self.mouse_state == MouseStates.CLICKED:
            self.text_buffer += f"{self.mouse_x} {self.mouse_y}"
            self.drawing_line_end(self.text_buffer)
            self.mouse_state = MouseStates.CLEAR
            self.text_buffer = ""

    def draw_circle_using_mouse_pointer(self, event):
        self.set_mouse_coordinates(event)

        if self.mouse_state == MouseStates.CLEAR:
            self.text_buffer += f"{self.mouse_x} {self.mouse_y} "
            self.mouse_state = MouseStates.CLICKED

        elif self.mouse_state == MouseStates.CLICKED:
            temp_text_buffer = self.text_buffer + f"{self.mouse_x} {self.mouse_y}"
            origin_x, origin_y, circf_x, circf_y = temp_text_buffer.split(" ")
            radius = int(util.calc_length(origin_x, origin_y, circf_x, circf_y))
            self.text_buffer += f"{radius}"
            self.drawing_circle_end(self.text_buffer)
            self.mouse_state = MouseStates.CLEAR
            self.text_buffer = ""

    def cmd_output_print(self, text):
        self.cmd_output.insert(END, text + '\n')

    def cmd_output_print_error_invalid_command(self):
        self.cmd_output_print('Invalid command!')

    def parse_command(self, text):
        self.cmd_output_print('calling ' + self.input_var.get() + '...')

        commands = {'line': self.drawing_line_start,
                    'circle': self.drawing_circle_start,
                    'close': self.close_window
                    }
        result = util.switch_dict(text, commands, default=self.cmd_output_print_error_invalid_command)
        return result()

    def do_action(self, text):
        states = {States.CLEAR: self.parse_command,
                  States.WAIT_LINE_COORDINATES: self.drawing_line_end,
                  States.WAIT_CIRCLE_COORDINATES: self.drawing_circle_end
                  }
        result = util.switch_dict(self.state, states)
        return result(text)

    def procedure(new_state):
        def execute(func):
            @wraps(func)
            def inner(self, *args, **kwargs):
                try:
                    result = func(self, *args, **kwargs)
                    self.state = new_state
                    return result
                except Exception as ex:
                    # TODO: reduce number of exceptions covered with this block
                    self.cmd_output_print('Error! Please try again.')
                    print(ex)

            return inner

        return execute

    @procedure(new_state=States.WAIT_LINE_COORDINATES)
    def drawing_line_start(self):
        print('line')
        self.cmd_output_print('drawing line...')
        self.cmd_output_print('Input coordinates')
        self.cmd_output_print('format: start_x, start_y, end_x, end_y')

    @procedure(new_state=States.CLEAR)
    def drawing_line_end(self, text):
        start_x, start_y, end_x, end_y = text.split(" ")
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5)
        self.cmd_output_print('line drawn')

    @procedure(new_state=States.WAIT_CIRCLE_COORDINATES)
    def drawing_circle_start(self):
        print('circle')
        self.cmd_output_print('drawing circle...')
        self.cmd_output_print('Input coordinates')
        self.cmd_output_print('format: origin_x, origin_y, radius')

    @procedure(new_state=States.CLEAR)
    def drawing_circle_end(self, text):
        origin_x, origin_y, radius = text.split(" ")
        self.canvas.create_circle(origin_x, origin_y, radius, fill="blue", width=4)
        self.cmd_output_print('circle drawn')


a = MainWindow(0)
a.root.mainloop()
