#!/usr/bin/env python3

from enum import Enum


"""
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