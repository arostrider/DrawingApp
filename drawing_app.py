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


def procedure_step(new_state=None, new_mouse_state=None):
    """Decorator warp methods that change state variable of MainWindow class instance."""

    def execute(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                if new_state is not None:
                    self.state = new_state
                if new_mouse_state is not None:
                    self.mouse_state = new_mouse_state
                return result
            except Exception as ex:
                # TODO: reduce number of exceptions covered with this block
                # TODO: how do I want to print error message?
                self.cmd_output_print('Error! Please try again.')
                print(ex)

        return inner

    return execute


# TODO: implement elements (greda, oslonac, sila, zglob...) as classes

# TODO: organize widgets among frames
# TODO: setup grid as geometry manager instead of place

# TODO: think of splitting drawing line into two parts (start and end point coordinates input)


print("Hello World")


class MainWindow:
    def __init__(self, parent):
        """When the class is instanced, initialize instance variables holding information about:
        mouse coordinates, buffers, state machines.
        At the end, create gui design and bind keys."""
        self.mouse_x, self.mouse_y = 0, 0
        self.text_buffer = ""

        self.state = States.CLEAR
        self.mouse_state = MouseStates.CLEAR

        self.gui_design(parent)
        self.bind_keys()

    def gui_design(self, parent):
        """Window design."""
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
        self.button_close = ttk.Button(self.root, text="Close", style='button_text_style.TButton', cursor="arrow",
                                       state="normal")
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
        """Configure key bindings for windows widgets."""
        self.cmd_input.bind('<Return>', lambda event: self.cmd_enter())
        self.canvas.bind('<Motion>', lambda event: self.mouse_over_canvas(event))
        self.canvas.bind('<Button-1>', lambda event: self.mouse_left_click_canvas(event))

    def close_window(self):
        """Destroy the window, then kill the program."""
        self.root.destroy()
        print('window closed')
        sys.exit()

    def cmd_enter(self):
        """Pull the text from the command input textbox, then clear it."""
        cmd_input_text = self.cmd_input.get()
        self.do_action(cmd_input_text)
        self.cmd_input.delete(0, tk.END)

    def set_mouse_coordinates(self, event):
        """Utility method: set instance variables (self.x, self.y) value to mouse pointer current position coordinates."""
        self.mouse_x, self.mouse_y = event.x, event.y

    def mouse_over_canvas(self, event):
        """Change the text on canvas to reflect mouse pointer current position coordinates."""
        # TODO: find way to adapt text color to its lower layer color
        self.set_mouse_coordinates(event)

        self.canvas.itemconfigure(self.canvas_text_mouse_x, text=f"X: {self.mouse_x}")
        self.canvas.itemconfigure(self.canvas_text_mouse_y, text=f"Y: {self.mouse_y}")
        self.canvas.tag_raise(self.canvas_text_mouse_x)
        self.canvas.tag_raise(self.canvas_text_mouse_y)

    # TODO
    def dynamic_drawing_line(self, event):
        # TODO
        self.set_mouse_coordinates(event)
        start_x, start_y = self.mouse_x, self.mouse_y
        self.state = States.WAIT_LINE_COORDINATES
        while self.state == States.WAIT_LINE_COORDINATES:
            self.set_mouse_coordinates(event)
            end_x, end_y = self.mouse_x, self.mouse_y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5)

    def mouse_left_click_canvas(self, event):
        """Event handler: mouse left click on canvas."""
        if self.state == States.CLEAR:
            return

        mouse_left_click_procedure_steps = {States.WAIT_LINE_COORDINATES: self.draw_line_using_mouse_pointer,
                                            States.WAIT_CIRCLE_COORDINATES: self.draw_circle_using_mouse_pointer
                                            }
        result = util.switch_dict(self.state, mouse_left_click_procedure_steps)
        result(event)
        print(self.mouse_state)
        # return result(event)

    def draw_element_using_mouse_pointer(self, event, element_drawing_procedure_dict):
        """Mouse drawing procedure handler encapsulation
        :param event
            just pass event (it is a tkinter thing)
        :param element_drawing_procedure_dict
            Use dictionary as switch data to determine next action according to mouse state instance variable (self.mouse_state)."""
        self.set_mouse_coordinates(event)
        result = util.switch_dict(self.mouse_state, element_drawing_procedure_dict)
        return result()

    def draw_line_using_mouse_pointer(self, event):
        """Draw line using mouse procedure handler
        :param event
            just pass event (it is a tkinter thing)"""
        line_procedure_steps = {MouseStates.CLEAR: self.mouse_click_input_first_coordinate,
                                MouseStates.CLICKED: self.mouse_click_input_second_coordinate_line
                                }
        self.draw_element_using_mouse_pointer(event, line_procedure_steps)

    def draw_circle_using_mouse_pointer(self, event):
        """Draw circle using mouse procedure handler
        :param event
            just pass event (it is a tkinter thing)"""
        circle_procedure_steps = {MouseStates.CLEAR: self.mouse_click_input_first_coordinate,
                                  MouseStates.CLICKED: self.mouse_click_input_second_coordinate_circle
                                  }
        self.draw_element_using_mouse_pointer(event, circle_procedure_steps)

    @procedure_step(new_mouse_state=MouseStates.CLICKED)
    def mouse_click_input_first_coordinate(self):
        self.text_buffer += f"{self.mouse_x} {self.mouse_y} "

    @procedure_step(new_mouse_state=MouseStates.CLEAR)
    def mouse_click_input_second_coordinate_line(self):
        self.text_buffer += f"{self.mouse_x} {self.mouse_y}"
        self.drawing_line_end(self.text_buffer)
        self.text_buffer = ""

        # TODO: think if this block should enable dynamic view while drawing using mouse
        '''
        start_x, start_y = self.mouse_x, self.mouse_y
        while self.mouse_state == MouseStates.CLICKED:
            self.set_mouse_coordinates(event)
            end_x, end_y = self.mouse_x, self.mouse_y
            self.canvas.bind('<Motion>',
                             lambda: self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5))
        '''

    @procedure_step(new_mouse_state=MouseStates.CLEAR)
    def mouse_click_input_second_coordinate_circle(self):
        temp_text_buffer = self.text_buffer + f"{self.mouse_x} {self.mouse_y}"
        origin_x, origin_y, circf_x, circf_y = temp_text_buffer.split(" ")
        radius = int(util.calc_length(origin_x, origin_y, circf_x, circf_y))
        self.text_buffer += f"{radius}"
        self.drawing_circle_end(self.text_buffer)
        self.text_buffer = ""

    def cmd_output_print(self, message_text):
        """Print message in window command output textbox widget."""
        self.cmd_output.insert(tk.END, message_text + '\n')

    def cmd_output_print_error_invalid_command(self):
        """Print error message in window command output textbox widget."""
        self.cmd_output_print('Invalid command!')

    def parse_command(self, cmd_text):
        """Get command input text, parse it, then determine which method to call."""
        self.cmd_output_print('calling ' + self.input_var.get() + '...')

        commands = {'line': self.drawing_line_start,
                    'circle': self.drawing_circle_start,
                    'close': self.close_window
                    }
        result = util.switch_dict(cmd_text, commands, default=self.cmd_output_print_error_invalid_command)
        return result()

    def do_action(self, cmd_text):
        """Determine which action to do next according to instances state machine variable (self.state)."""
        states = {States.CLEAR: self.parse_command,
                  States.WAIT_LINE_COORDINATES: self.drawing_line_end,
                  States.WAIT_CIRCLE_COORDINATES: self.drawing_circle_end
                  }
        result = util.switch_dict(self.state, states)
        return result(cmd_text)

    @procedure_step(new_state=States.WAIT_LINE_COORDINATES)
    def drawing_line_start(self):
        print('line')
        self.cmd_output_print('drawing line...')
        self.cmd_output_print('Input coordinates')
        self.cmd_output_print('format: start_x, start_y, end_x, end_y')

    @procedure_step(new_state=States.CLEAR)
    def drawing_line_end(self, text):
        start_x, start_y, end_x, end_y = text.split(" ")
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5)
        self.cmd_output_print('line drawn')

    @procedure_step(new_state=States.WAIT_CIRCLE_COORDINATES)
    def drawing_circle_start(self):
        print('circle')
        self.cmd_output_print('drawing circle...')
        self.cmd_output_print('Input coordinates')
        self.cmd_output_print('format: origin_x, origin_y, radius')

    @procedure_step(new_state=States.CLEAR)
    def drawing_circle_end(self, text):
        origin_x, origin_y, radius = text.split(" ")
        self.canvas.create_circle(origin_x, origin_y, radius, fill="blue", width=4)
        self.cmd_output_print('circle drawn')


def main():
    a = MainWindow(0)
    a.root.mainloop()


if __name__ == '__main__':
    main()
