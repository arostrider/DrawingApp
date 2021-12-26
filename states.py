from enum import Enum


class States(Enum):
    CLEAR = 0
    WAIT_LINE_COORDINATES = 1
    WAIT_CIRCLE_COORDINATES = 2


class MouseStates(Enum):
    CLEAR = 0
    CLICKED = 1
