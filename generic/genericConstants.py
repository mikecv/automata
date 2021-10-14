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


class ControllerScope(Enum):
    """
    Controller scope (redundancy).
    """
    STANDBY = 0
    PRIMARY = 1
