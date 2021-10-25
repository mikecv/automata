#!/usr/bin/env python3

from abc import ABC, abstractmethod
import logging

from generic.genericConstants import *


class GenericIO():   
    """
    Class to represent a generic Input/Output (I/O).
    """

    def __init__(self, log: logging, ioType: IOType, activeState: ActiveState) -> None:
        """
        Initialisation method.
        Parameters:
            log : Shared logging object.
            ioType : Input/Output type.
            activeState : Active state, high or low.
        """

        self.log = log

        # Initialise IO.
        self.ioType = ioType
        self.activeState = activeState
        self._active = False
        self._level = Level.LOW

        # Initialise digital input.
        self.initialise()    

    @property
    def active(self) -> None:
        """
        Getter property for input state (active or not).
        """
        return self._active

    @property
    def level(self) -> None:
        """
        Getter property for input level (high or low).
        """
        return self._level

    @level.setter
    def level(self, l) -> None:
        """
        Setter property for input level (high or low).
        Level and active state are related, so only level can be set;
        the active state will be set here accordingly.
        """
        self._level = l

        # Set active state accordingly.
        # If level is the same as the active state then input is active.
        if l == Level.LOW:
            if self.activeState == ActiveState.ACTIVE_LOW:
                self._active = True
            else:
                self._active = False
        else:
            if self.activeState == ActiveState.ACTIVE_LOW:
                self._active = False
            else:
                self._active = True

    def initialise(self) -> None:
        """
        Initialise Input/Output (I/O).
        """

        self.log.debug(f'Performing generic IO initialisation for : {self.ioType}')
        
        # Initialise input to low level state.
        # The setter property should set the active state accordingly.
        self.level = Level.LOW

