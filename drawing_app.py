import sys
import util
import pprint
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
from functools import wraps

from states import States, MouseStates
from elements import Line, Circle, Greda, Zglob, Sila
from grid_points_generator import GridPointsGenerator


def create_circle(self, x, y, r, **kwargs):
    """Custom, more intuitive method for drawing circle on tkinter.Canvas"""
    try:
        x, y, r = int(x), int(y), int(r)
    except ValueError as ex:
        print(ex)

    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def move_to_specified_coordinates(self, canvas_object, x, y, **kwargs):
    """Custom, more intuitive method for moving element on tkinter.Canvas"""
    try:
        x, y = int(x), int(y)
    except ValueError as ex:
        print(ex)

    start_x, start_y = self.coords(canvas_object)[:2]
    move_x = x - start_x
    move_y = y - start_y
    print(f"Moving from {start_x}, {start_y}")
    print(f"Moving by x: {move_x}, y: {move_y}")
    return self.move(canvas_object, move_x, move_y, **kwargs)


# adding methods to tkinter module
tkinter.Canvas.create_circle = create_circle
tkinter.Canvas.move_to_specified_coordinates = move_to_specified_coordinates


def procedure_step(new_state=None, new_mouse_state=None):
    """Decorator wraps methods that change state variable of MainWindow class instance."""

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
                if 'cancel' in args:
                    print('cancel')
                self.cmd_output_print('Error! Please try again.')
                print(ex)
                raise ex

        return inner

    return execute


class IDCounter:
    def __init__(self):
        self.element_id_count = 0

    def issue_new_id(self):
        """Increment ID counter, return new ID.
        :returns
                New ID value (self.element_id_count + 1)"""
        new_id = self.element_id_count + 1
        self.element_id_count += 1
        return new_id


ID_COUNTER = IDCounter()


def init_new():
    """Decorator wraps methods that are used to create instance of new elements.Element child class."""

    def execute(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            try:
                element_id = ID_COUNTER.issue_new_id()
                new_object = func(self, element_id, *args, **kwargs)
                self.drawn_elements.append(new_object)
                # TODO: repace word new with actual object name (greda, sila, etc.)
                self.cmd_output_print(f"Drawn new element with id {element_id}")
            except Exception as ex:
                # TODO: reduce number of exceptions covered with this block
                # TODO: how do I want to print error message?
                if 'cancel' in args:
                    print('cancel')
                self.cmd_output_print('Error! Please try again.')
                print(ex)
                raise ex

        return inner

    return execute

# TODO: undo and redo functionalities
# TODO: implement greda, zglob and sila drawing using mouse pointer

# TODO: elements drawing must be tied to grid points

# TODO: implement element Oslonac as a class

# TODO: fancy dynamic element drawing

# TODO: organize widgets among frames
# TODO: setup grid as geometry manager instead of place

# TODO: make clicked point fixated to the cursor while moving?
# TODO: split drawing line into two parts (start and end point coordinates input)?
# TODO: optimize action flows by implementing mouse release flag?


print("Prerequisite modules imported!")


class MainWindow:
    GRID_STEP_X, GRID_STEP_Y = 20, 20

    def __init__(self, parent):
        """When the class is instanced, initialize instance variables holding information about:
        mouse coordinates, buffers, state machines.
        At the end, create gui design and bind keys."""
        self.mouse_x, self.mouse_y = 0, 0
        self.text_buffer = ""

        self.element_id_count = 0
        self.drawn_elements = [None]
        self.selected_element = None

        self.state = States.CLEAR
        self.mouse_state = MouseStates.CLEAR

        self.gui_design(parent)
        self.bind_keys()

        self.grid_generator = self.init_grid_points_generator_object()

        self.canvas_grid_points = list(self.grid_generator())

        pprint.pp(self.canvas_grid_points)

    def init_grid_points_generator_object(self):
        return GridPointsGenerator(height=self.canvas.winfo_height(), width=self.canvas.winfo_width(),
                                   step_x=self.GRID_STEP_X, step_y=self.GRID_STEP_Y)

    def canvas_draw_grid(self):
        self.canvas.update()
        grid_generator = self.init_grid_points_generator_object()

        points_N = grid_generator.generate_N_border_points()
        points_S = grid_generator.generate_S_border_points()
        points_E = grid_generator.generate_E_border_points()
        points_W = grid_generator.generate_W_border_points()

        for p_N, p_S in zip(points_N, points_S):
            self.canvas.create_line(*p_N, *p_S, width=0.25, fill="grey")

        for p_W, p_E in zip(points_W, points_E):
            self.canvas.create_line(*p_W, *p_E, width=0.25, fill="grey")

    def gui_design(self, parent):
        """Window design."""
        self.root = tk.Tk()
        self.root.geometry('500x570+520+200')

        self.root = ttk.Frame(parent)
        self.root.place(x=0, y=0, width=500, height=570)

        # drawing canvas
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.place(x=10, y=7, width=480, height=370)

        # mouse coordinates as text on canvas
        self.canvas_text_mouse_x = self.canvas.create_text(400, 355, text=f"X: {self.mouse_x}", anchor=tk.W)
        self.canvas_text_mouse_y = self.canvas.create_text(440, 355, text=f"Y: {self.mouse_y}", anchor=tk.W)

        # draw on canvas
        self.canvas_draw_grid()

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

        if cmd_input_text == 'cancel':
            self.cancel_action_reset_states()

        self.do_action(cmd_input_text)
        self.cmd_input.delete(0, tk.END)

    def clear_text_buffer(self):
        """Utility method: clears text buffer."""
        self.text_buffer = ""

    def set_mouse_coordinates(self, event):
        """Utility method: set instance variables (self.x, self.y) value to mouse pointer current position coordinates."""
        self.mouse_x, self.mouse_y = event.x, event.y

        self.canvas.itemconfigure(self.canvas_text_mouse_x, text=f"X: {self.mouse_x}")
        self.canvas.itemconfigure(self.canvas_text_mouse_y, text=f"Y: {self.mouse_y}")
        self.canvas.tag_raise(self.canvas_text_mouse_x)
        self.canvas.tag_raise(self.canvas_text_mouse_y)

    def mouse_over_canvas(self, event):
        """Change the text on canvas to reflect mouse pointer current position coordinates."""
        # TODO: find way to adapt text color to its lower layer color
        self.set_mouse_coordinates(event)

    def mouse_left_click_canvas(self, event):
        """Event handler: mouse left click on canvas.
        :raise
            ValueError if current self.state value is not in mouse_left_click_procedure_steps.keys()."""
        self.set_mouse_coordinates(event)
        closest_point = self.grid_generator.find_closest_grid_point((self.mouse_x, self.mouse_y))
        print(f'Closest point is: grid{closest_point}, '
              f'pixels{self.grid_generator.convert_grid_point_to_pixel_coordinated_point(closest_point)}')

        if self.state == States.CLEAR:
            return

        mouse_left_click_procedure_steps = {States.WAIT_LINE_COORDINATES: self.draw_line_using_mouse_pointer,
                                            States.WAIT_CIRCLE_COORDINATES: self.draw_circle_using_mouse_pointer,
                                            States.WAIT_GREDA_COORDINATES: self.draw_greda_using_mouse_pointer
                                            }
        result = util.switch_dict(self.state, mouse_left_click_procedure_steps,
                                  default=lambda ex: util.raise_undefined_behaviour(ValueError,
                                                                                    "self.mouse_left_click_canvas"))
        result(event)
        print(self.mouse_state)
        # return result(event)

    def draw_element_using_mouse_pointer(self, event, element_drawing_procedure_dict):
        """Mouse drawing procedure handler encapsulation
                :param event
                    just pass event (it is a tkinter thing)
                :param element_drawing_procedure_dict
                    Use dictionary as switch data to determine next action according to mouse state instance variable (self.mouse_state)."""
        # self.set_mouse_coordinates(event)
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

    # TODO: implement greda, zglob and sila drawing using mouse pointer
    def draw_greda_using_mouse_pointer(self, event):
        """Draw greda using mouse procedure handler
                :param event
                    just pass event (it is a tkinter thing)"""
        greda_procedure_steps = {MouseStates.CLEAR: self.mouse_click_input_first_coordinate,
                                 MouseStates.CLICKED: self.mouse_click_input_second_coordinate_greda
                                 }
        self.draw_element_using_mouse_pointer(event, greda_procedure_steps)

    def draw_zglob_using_mouse_pointer(self, event):
        """Draw zglob using mouse procedure handler
                :param event
                    just pass event (it is a tkinter thing)"""
        zglob_procedure_steps = {MouseStates.CLEAR: self.mouse_click_input_first_coordinate,
                                 MouseStates.CLICKED: self.mouse_click_input_second_coordinate_zglob
                                 }
        self.draw_element_using_mouse_pointer(event, zglob_procedure_steps)

    def draw_sila_using_mouse_pointer(self, event):
        """Draw greda using mouse procedure handler
                :param event
                    just pass event (it is a tkinter thing)"""
        sila_procedure_steps = {MouseStates.CLEAR: self.mouse_click_input_first_coordinate,
                                MouseStates.CLICKED: self.mouse_click_input_second_coordinate_sila
                                }
        self.draw_element_using_mouse_pointer(event, sila_procedure_steps)

    @procedure_step(new_mouse_state=MouseStates.CLICKED)
    def mouse_click_input_first_coordinate(self):
        self.text_buffer += f"{self.mouse_x} {self.mouse_y} "

    @procedure_step(new_mouse_state=MouseStates.CLEAR)
    def mouse_click_input_second_coordinate_line(self):
        self.text_buffer += f"{self.mouse_x} {self.mouse_y}"
        self.drawing_line_end(self.text_buffer)
        self.clear_text_buffer()

    @procedure_step(new_mouse_state=MouseStates.CLEAR)
    def mouse_click_input_second_coordinate_circle(self):
        temp_text_buffer = self.text_buffer + f"{self.mouse_x} {self.mouse_y}"
        origin_x, origin_y, circf_x, circf_y = temp_text_buffer.split(" ")
        radius = int(util.calc_length(origin_x, origin_y, circf_x, circf_y))
        self.text_buffer += f"{radius}"
        self.drawing_circle_end(self.text_buffer)
        self.clear_text_buffer()

    @procedure_step(new_mouse_state=MouseStates.CLEAR)
    def mouse_click_input_second_coordinate_greda(self):
        self.text_buffer += f"{self.mouse_x} {self.mouse_y}"
        coords = list(map(int, self.text_buffer.split(" ")))
        angle = round(
            util.degrees(
                util.calc_angle_between_line_and_positive_x_axis_and_round_to_nearest_eighth(*coords)
            )
        )
        print(f'Ugao: {angle}')
        length = round(util.calc_length(*coords))
        print(f'Duzina: {length}')
        start_x, start_y = coords[0:2]
        buffer = f"{start_x} {start_y} {angle} {length}"
        self.drawing_greda_end(buffer)
        self.clear_text_buffer()

    def cmd_output_print(self, message_text):
        """Print message in window command output textbox widget."""
        self.cmd_output.insert(tk.END, message_text + '\n')

    def cmd_output_print_error_invalid_command(self):
        """Print error message in window command output textbox widget."""
        self.cmd_output_print('Invalid command!')

    def parse_command(self, cmd_text):
        """Get command input text, parse it, then determine which method to call."""
        if cmd_text == 'cancel':
            return

        self.cmd_output_print('calling ' + self.input_var.get() + '...')

        commands = {'line': self.drawing_line_start,
                    'circle': self.drawing_circle_start,
                    'close': self.close_window,
                    'get selected': self.cmd_output_print_selected,
                    'delete': self.delete_selected_element,
                    'move': self.move_selected_element_start,
                    'greda': self.drawing_greda_start,
                    'zglob': self.drawing_zglob_start,
                    'sila': self.drawing_sila_start
                    }
        result = util.switch_dict(cmd_text, commands, default=self.cmd_output_print_error_invalid_command)
        return result()

    def do_action(self, cmd_text):
        """Determine which action to do next according to instances state machine variable (self.state)."""
        states = {States.CLEAR: self.parse_command,
                  States.WAIT_LINE_COORDINATES: self.drawing_line_end,
                  States.WAIT_CIRCLE_COORDINATES: self.drawing_circle_end,
                  States.WAIT_MOVE_COORDINATES: self.move_selected_element_end,
                  States.WAIT_GREDA_COORDINATES: self.drawing_greda_end,
                  States.WAIT_ZGLOB_COORDINATES: self.drawing_zglob_end,
                  States.WAIT_SILA_COORDINATES: self.drawing_sila_end
                  }
        result = util.switch_dict(self.state, states)
        return result(cmd_text)

    @procedure_step(new_state=States.WAIT_GREDA_COORDINATES)
    def drawing_greda_start(self):
        print('greda')
        self.cmd_output_print('Input start coordinates, direction and length')
        self.cmd_output_print('format: start_x, start_y, direction_angle, length')

    @procedure_step(new_state=States.CLEAR)
    def drawing_greda_end(self, text):
        self.cmd_output_print('drawing greda...')
        start_x, start_y, direction, length = list(map(int, text.split(" ")))
        direction = round(
            util.degrees(
                util.round_angle_to_nearest_eighth(util.radians(direction))
            )
        )
        self.init_new_greda(start_x, start_y, length, direction)

    @procedure_step(new_state=States.WAIT_SILA_COORDINATES)
    def drawing_sila_start(self):
        print('sila')
        self.cmd_output_print('Input start coordinates, direction and length')
        self.cmd_output_print('format: attack_x, attack_y, attack_angle, intensity')

    @procedure_step(new_state=States.CLEAR)
    def drawing_sila_end(self, text):
        self.cmd_output_print('drawing sila...')
        attack_x, attack_y, attack_angle, intensity = list(map(int, text.split(" ")))
        attack_angle = round(
            util.degrees(
                util.round_angle_to_nearest_eighth(util.radians(attack_angle))
            )
        )
        self.init_new_sila(attack_x, attack_y, attack_angle, intensity)

    @procedure_step(new_state=States.WAIT_LINE_COORDINATES)
    def drawing_line_start(self):
        print('line')
        self.cmd_output_print('Input coordinates')
        self.cmd_output_print('format: start_x, start_y, end_x, end_y')

    @procedure_step(new_state=States.CLEAR)
    def drawing_line_end(self, text):
        self.cmd_output_print('drawing line...')
        start_x, start_y, end_x, end_y = text.split(" ")
        self.init_new_line(start_x, start_y, end_x, end_y, fill="green", width=4)

    @procedure_step(new_state=States.WAIT_CIRCLE_COORDINATES)
    def drawing_circle_start(self):
        print('circle')
        self.cmd_output_print('Input coordinates')
        self.cmd_output_print('format: origin_x, origin_y, radius')

    @procedure_step(new_state=States.CLEAR)
    def drawing_circle_end(self, text):
        self.cmd_output_print('drawing circle...')
        origin_x, origin_y, radius = text.split(" ")
        self.init_new_circle(origin_x, origin_y, radius, fill="blue", width=2)

    @procedure_step(new_state=States.WAIT_ZGLOB_COORDINATES)
    def drawing_zglob_start(self):
        print('zglob')
        self.cmd_output_print('Input coordinates')
        self.cmd_output_print('format: origin_x, origin_y')

    @procedure_step(new_state=States.CLEAR)
    def drawing_zglob_end(self, text):
        # TODO: implement other draw_element_end functions like this
        #       calculate_closest_canvas_pixel_coordinated_grid_point(x, y) -> int, int
        self.cmd_output_print('drawing zglob...')
        origin_x, origin_y = text.split(" ")
        grid_x, grid_y = self.grid_generator.find_closest_grid_point((origin_x, origin_y))
        grid_origin_x, grid_origin_y = self.grid_generator.convert_grid_point_to_pixel_coordinated_point((grid_x, grid_y))

        print(grid_origin_x)
        print(grid_origin_y)
        self.init_new_zglob(grid_origin_x, grid_origin_y)

    @procedure_step(new_state=States.WAIT_MOVE_COORDINATES)
    def move_selected_element_start(self):
        print('move')
        self.cmd_output_print('moving element...')
        self.cmd_output_print('Input coordinates')
        self.cmd_output_print('format: new_x, new_y')

    @procedure_step(new_state=States.CLEAR)
    def move_selected_element_end(self, text):
        new_x, new_y = text.split(" ")
        self.move_element(self.selected_element, new_x, new_y)

    @procedure_step(new_state=States.CLEAR, new_mouse_state=MouseStates.CLEAR)
    def cancel_action_reset_states(self):
        self.clear_text_buffer()
        self.cmd_output_print("Action cancelled.")

    @init_new()
    def init_new_greda(self, element_id, start_x, start_y, direction, length):
        return Greda(element_id, self.canvas, self, start_x, start_y, length, direction)

    @init_new()
    def init_new_zglob(self, element_id, origin_x, origin_y):
        return Zglob(element_id, self.canvas, self, origin_x, origin_y)

    @init_new()
    def init_new_sila(self, element_id, attack_x, attack_y, attack_angle, intensity):
        return Sila(element_id, self.canvas, self, attack_x, attack_y, attack_angle, intensity)

    # TODO: issue_new_id and init_new functions below are redundant, but please check when removing
    def issue_new_id(self):
        """Increment ID counter, return new ID.
        :returns
                New ID value (self.element_id_count + 1)"""
        new_id = self.element_id_count + 1
        self.element_id_count += 1
        return new_id

    def init_new_line(self, start_x, start_y, end_x, end_y, **kwargs):
        """Line drawing master handler.
                Generate line object with new ID, append it to elements list (self.drawn_elements)."""
        element_id = self.issue_new_id()
        new_line = Line(element_id, self.canvas, self, start_x, start_y, end_x, end_y, **kwargs)
        self.drawn_elements.append(new_line)
        self.cmd_output_print(f"Drawn line element with id {element_id}")
        return new_line

    def init_new_circle(self, origin_x, origin_y, radius, **kwargs):
        """Circle drawing master handler.
                Generate circle object with new ID, append it to elements list (self.drawn_elements)."""
        element_id = self.issue_new_id()
        new_circle = Circle(element_id, self.canvas, self, origin_x, origin_y, radius, **kwargs)
        self.drawn_elements.append(new_circle)
        self.cmd_output_print(f"Drawn circle element with id {element_id}")
        return new_circle

    def cmd_output_print_selected(self):
        """Loging method."""
        if self.selected_element:
            self.cmd_output_print(f'{self.selected_element} with ID {self.selected_element.id} is selected!')
        else:
            self.cmd_output_print('No element is selected!')

    def delete_element(self, element):
        """Delete element master handler.
                        Remove element object from the list (self.drawn_elements), insert placeholder to keep ID mechanics consistent, delete it from canvas."""
        if element not in self.drawn_elements:
            raise ValueError("element not found")

        self.drawn_elements.pop(element.id)
        self.drawn_elements.insert(element.id, None)
        self.canvas.delete(element.image)
        self.cmd_output_print(f"Deleted element with ID {element.id}")

    def delete_selected_element(self):
        """Wraps self.delete_element to delete currently selected element (self.selected_element)."""
        self.delete_element(self.selected_element)

    def move_element(self, element, new_x, new_y):
        """Move element to specified coordinates."""
        new_x, new_y = int(new_x), int(new_y)

        if type(element) == Circle or type(element) == Zglob:
            """Handle moving circle and zglob so that argument coordinates point to the circle origin."""
            new_x = new_x - element.radius
            new_y = new_y - element.radius

        self.canvas.move_to_specified_coordinates(element.image, new_x, new_y)


def main():
    a = MainWindow(0)
    a.root.mainloop()


if __name__ == '__main__':
    main()
