import sys
import util
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
from functools import wraps
from states import States, MouseStates


def create_circle(self, x, y, r, **kwargs):
    """Custom, more intuitive method for drawing circle on tkinter.Canvas"""
    # TODO: is this try/catch block really needed?
    try:
        x, y, r = int(x), int(y), int(r)
    except ValueError as ex:
        print(ex)

    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


# adding a method to tkinter library
tkinter.Canvas.create_circle = create_circle


def procedure(new_state):
    """This decorator is used on methods that are changing state variable of MainWindow class instance."""
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

# TODO: think about adding new_mouse_state argument to procedure decorator
# TODO: implement elements (greda, oslonac, sila, zglob...) as classes

# TODO: organize widgets among frames
# TODO: setup grid as geometry manager instead of place

# TODO: think of splitting drawing line into two parts (start and end point coordinates input)


print("Hello World")


class MainWindow:
    def __init__(self, parent):
        self.mouse_x, self.mouse_y = 0, 0
        self.gui(parent)
        self.bind_keys()

        self.mouse_state = MouseStates.CLEAR

        self.state = States.CLEAR

        self.text_buffer = ""

    def gui(self, parent):

        self.root = tk.Tk()
        self.root.geometry('500x570')

        self.root = ttk.Frame(parent)
        self.root.place(x=0, y=0, width=500, height=570)

        # drawing canvas
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.place(x=10, y=7, width=480, height=370)

        # mouse coordinates as text on canvas
        self.canvas_text_mouse_x = self.canvas.create_text(400, 355, text=f"X: {self.mouse_x}", anchor=tk.W)
        self.canvas_text_mouse_y = self.canvas.create_text(440, 355, text=f"Y: {self.mouse_y}", anchor=tk.W)

        # output text box
        self.cmd_output = tk.Text(self.root, bg="#000000", fg="#ffffff",
                                  font=tkinter.font.Font(family="Consolas", size=10),
                                  cursor="arrow", state="normal")
        self.cmd_output.place(x=10, y=380, width=480, height=120)

        self.button_text_style = ttk.Style()
        self.button_text_style.configure('button_text_style.TButton', font=('Consolas', 10), foreground='black')

        # closing button
        # TODO: in progress
        self.button_close = ttk.Button(self.root, text="Close", style='button_text_style.TButton', cursor="arrow", state="normal")
        self.button_close.place(x=400, y=530, width=90, height=32)
        self.button_close['command'] = self.close_window

        # input text box
        self.input_var = tk.StringVar()
        self.cmd_input = ttk.Entry(self.root, textvariable=self.input_var, background="black", foreground="black",
                                   font=tkinter.font.Font(family="Consolas", size=10),
                                   cursor="arrow", state="normal")
        self.cmd_input.place(x=60, y=500, width=429, height=22)

        # enter button
        self.button_enter = ttk.Button(self.root, text=">>>", style='button_text_style.TButton',
                                       cursor="arrow",
                                       state="normal")
        self.button_enter.place(x=10, y=499, width=50, height=24)
        self.button_enter['command'] = self.cmd_enter

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
        self.cmd_input.delete(0, tk.END)

    def set_mouse_coordinates(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y

    def mouse_over_canvas(self, event):
        # TODO: find way to adapt text color to its lower layer color
        self.set_mouse_coordinates(event)

        self.canvas.itemconfigure(self.canvas_text_mouse_x, text=f"X: {self.mouse_x}")
        self.canvas.itemconfigure(self.canvas_text_mouse_y, text=f"Y: {self.mouse_y}")
        self.canvas.tag_raise(self.canvas_text_mouse_x)
        self.canvas.tag_raise(self.canvas_text_mouse_y)

    def mouse_left_click_canvas(self, event):
        if self.state == States.CLEAR:
            pass

        elif self.state == States.WAIT_LINE_COORDINATES:
            self.draw_line_using_mouse_pointer(event)
            # self.dynamic_drawing_line(event)

        elif self.state == States.WAIT_CIRCLE_COORDINATES:
            self.draw_circle_using_mouse_pointer(event)

        print(self.mouse_state)

    def dynamic_drawing_line(self, event):
        # TODO
        self.set_mouse_coordinates(event)
        start_x, start_y = self.mouse_x, self.mouse_y
        self.state = States.WAIT_LINE_COORDINATES
        while self.state == States.WAIT_LINE_COORDINATES:
            self.set_mouse_coordinates(event)
            end_x, end_y = self.mouse_x, self.mouse_y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5)

    def draw_line_using_mouse_pointer(self, event):
        self.set_mouse_coordinates(event)

        if self.mouse_state == MouseStates.CLEAR:
            self.text_buffer += f"{self.mouse_x} {self.mouse_y} "
            self.mouse_state = MouseStates.CLICKED

        elif self.mouse_state == MouseStates.CLICKED:
            self.text_buffer += f"{self.mouse_x} {self.mouse_y}"

            # TODO: this block should enable dynamic view while drawing using mouse
            '''
            start_x, start_y = self.mouse_x, self.mouse_y
            while self.mouse_state == MouseStates.CLICKED:
                self.set_mouse_coordinates(event)
                end_x, end_y = self.mouse_x, self.mouse_y
                self.canvas.bind('<Motion>',
                                 lambda: self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5))
            '''

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
        self.cmd_output.insert(tk.END, text + '\n')

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
