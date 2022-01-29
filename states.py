from enum import Enum


class States(Enum):
    CLEAR = 0
    WAIT_LINE_COORDINATES = 1
    WAIT_CIRCLE_COORDINATES = 2
    WAIT_MOVE_COORDINATES = 3
    WAIT_GREDA_COORDINATES = 4
    WAIT_ZGLOB_COORDINATES = 5
    WAIT_SILA_COORDINATES = 6


class MouseStates(Enum):
    CLEAR = 0
    CLICKED = 1
