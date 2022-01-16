import re
from math import sqrt, cos, sin, radians


def calc_length(x0, y0, x1, y1):
    # TODO: can some library be used? eg. geomoeter, numpy
    """Calculates length(distance between two points) using Pythagoras theorem.

    :returns sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)"""
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    return sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def calc_vector_end_point(x0, y0, angle, length):
    x1 = x0 + length*cos(angle)
    y1 = y0 + length*sin(angle)
    return x1, y1


def rotate_rectangle(points, angle, center):
    angle = radians(angle)
    cos_val = cos(angle)
    sin_val = sin(angle)
    cx, cy = center
    new_points = []
    for x_old, y_old in points:
        x_old -= cx
        y_old -= cy
        x_new = x_old * cos_val - y_old * sin_val
        y_new = x_old * sin_val + y_old * cos_val
        new_points.append([x_new + cx, y_new + cy])
    return new_points


def switch_dict(value, _dict, default=None):
    # TODO: test this good! make better docstring
    """Iterates through dictionary treating it as a switch loop data where:
    keys are cases, and values are to be returned if its pairing case(dict key) is true."""
    for case in _dict.keys():
        if value == case:
            return _dict[case]

    return default


def is_string_matching_format(_string, _format):
    rex = re.compile(_format)
    if rex.match(_string):
        return True
    return False


def raise_undefined_behaviour(ex, obj_name, *args, **kwargs):
    """Raises exception to provide better insight on where behaviour should be defined."""
    raise ex(f"undefined behaviour {obj_name}")
