import re
from math import sqrt


def calc_length(x0, y0, x1, y1):
    # TODO: can some library be used? eg. geomoeter, numpy
    """Calculates length(distance between two points) using Pythagoras theorem.

    :returns sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)"""
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    return sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


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
