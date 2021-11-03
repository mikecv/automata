#!/usr/bin/env python3

from enum import Enum

""""
Generic constants defined here.
Application specific constants defined in specific application scope.
"""


class ControllerState(Enum):
    """
    Controller states.
    """
    STARTING = 0
    INITIALISING = 1
    ACTIVE = 2
    FAILED = 3
    TERMINATING = 4


class ControllerMode(Enum):
    """
    Controller modes.
    """
    OFF = 0
    ON = 1
    AUTO = 2
    MANUAL = 3


class ControllerModeReason(Enum):
    """
    Controller mode (fail) reasons.
    """
    NONE = 0
    NOT_ACTIVE = 1
    NO_CHANGE = 2


class ControllerScope(Enum):
    """
    Controller scope (redundancy).
    """
    STANDBY = 0
    PRIMARY = 1


class DigtialIoType(Enum):
    """
    Digital IO type (input or output)
    """
    DIGITAL_INPUT = 0
    DIGITAL_OUTPUT = 1


class ActiveLevel(Enum):
    """
    Digital IO active level
    """
    ACTIVE_LOW = 0
    ACTIVE_HIGH = 1


class Level(Enum):
    """
    Digital IO level
    """
    LOW = 0
    HIGH = 1