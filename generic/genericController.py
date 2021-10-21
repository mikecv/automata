#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Tuple

import sprinklers.ui_pb2 as ui_pb2

from generic.genericConstants import *


class GenericController():   
    """
    Class to represent a generic controller.
    """

    def __init__(self, name) -> None:
        """
        Initialisation method.
        """

        self.ctrlName = name

        # Initialise state/mode of the controller.
        self.stayAlive = True
        self.state = ControllerState.STARTING
        self.mode = ControllerMode.OFF

        # Initialise controller program to empty.
        # <TODO> Array of program entries.
        self.program = "Empty"

        # Initialise controller output states.
        # <TODO> this will be an object of an outputs class.
        self.outputs = "All Off"

    def stateMachine(self) -> None:
        """
        State machine method.
        Performs state transitions and invokes methods as required.
        """

        if self.state == ControllerState.STARTING:
            self.state = ControllerState.INITIALISING
        elif self.state == ControllerState.INITIALISING:
            self.initialise()
        elif self.state == ControllerState.ACTIVE:
            self.controlling()
        elif self.state == ControllerState.TERMINATING:
            self.stayAlive = False

    def initialise(self) -> None:
        """
        Initialise class variables and state.
        """

        # Initialise stay alive flag.
        self.stayAlive = True

        # Transition to the active state.
        self.state = ControllerState.ACTIVE

        # Initialise controller mode to OFF.
        self.mode = ControllerMode.OFF

    @abstractmethod
    def controlling(self) -> None:
        """
        Abstract method to perform controlling functions.
        This method must be overriden by specific controller class.
        """

        pass

    def setMode(self, reqMode: ControllerMode) -> Tuple[Enum, ControllerModeReason]:
        """
        Set the controller mode as required.
        Parameters:
            reqMode : Required controller mode (to set to).
        Returns:
            setStatus : Enum representing status of setting mode.
            setReason : Enum representing reason (used if setStatus not CD_GOOD)
        """

        # Initialise return status and failure reasons.
        setStatus = ui_pb2.UiModeStatus.CS_GOOD
        setReason = ControllerModeReason.NONE

        # Only all mode change if controller status is active.
        # Also, don't change if already set.
        if self.state == ControllerState.ACTIVE:
            if self.mode == reqMode:
                # Not setting new mode as unchanged.
                setStatus = ui_pb2.UiModeStatus.CS_MODE_FAIL
                setReason = ControllerModeReason.NO_CHANGE
            else:
                # Setting new mode.
                self.mode = reqMode
        else:
            # Failed to set mode
            setStatus = ui_pb2.UiModeStatus.CS_MODE_FAIL
            setReason = ControllerModeReason.NOT_ACTIVE

        return setStatus, setReason