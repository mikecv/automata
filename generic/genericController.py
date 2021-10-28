#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Tuple
import logging

import sprinklers.ui_pb2 as ui_pb2

from generic.genericConstants import *


class GenericController():   
    """
    Class to represent a generic controller.
    """

    def __init__(self, name: str, log: logging) -> None:
        """
        Initialisation method.
        Parameters:
            name : Name for this instance of generic controller.
            log : Shared logging object.
        """

        self._ctrlName = name
        self.log = log

        self.log.debug(f'Initialise generic controller for controller : {name}')

        # Initialise state/mode of the controller.
        self._stayAlive = True
        self._state = ControllerState.STARTING
        self._mode = ControllerMode.OFF

        # Initialise controller program to empty.
        # <TODO> Array of program entries.
        self.program = "Empty"

        # Initialise controller input states.
        # <TODO> this will be an object of an inputs class.
        self.inputs = "All Off"

        # Initialise controller output states.
        # <TODO> this will be an object of an outputs class.
        self.outputs = "All Off"

    @property
    def ctrlName(self) -> None:
        """
        Getter property for controller name.
        """
        return self._ctrlName

    @property
    def stayAlive(self) -> None:
        """
        Getter property for controller stayAlive flag.
        """
        return self._stayAlive

    @property
    def state(self) -> None:
        """
        Getter property for controller state.
        """
        return self._state

    @property
    def mode(self) -> None:
        """
        Getter property for controller mode.
        """
        return self._mode

    @ctrlName.setter
    def ctrlName(self, n) -> None:
        """
        Setter property for controller name.
        """
        self._ctrlName = n

    @stayAlive.setter
    def stayAlive(self, saf) -> None:
        """
        Setter property for controller stayAlive flag.
        """
        self._stayAlive = saf

    @state.setter
    def state(self, s) -> None:
        """
        Setter property for controller state.
        """
        self._state = s

    @mode.setter
    def mode(self, m) -> None:
        """
        Setter property for controller mode.
        """
        self._mode = m

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

        self.log.debug(f'Performing generic controller initialisation.')

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

        self.log.debug(f'Implementing control to set mode to : {reqMode}')

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
                self.log.debug(f'Attempting to set mode to existing mode.')
            else:
                # Setting new mode.
                self.mode = reqMode
        else:
            # Failed to set mode
            setStatus = ui_pb2.UiModeStatus.CS_MODE_FAIL
            setReason = ControllerModeReason.NOT_ACTIVE
            self.log.warning(f'Failed to set mode as controller not ACTIVE.')

        return setStatus, setReason