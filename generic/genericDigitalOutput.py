#!/usr/bin/env python3

from abc import ABC, abstractmethod
import logging

from generic.genericConstants import *


class GenericDigitalOutput():   
    """
    Class to represent a generic digital output.
    """

    def __init__(self, log: logging, activeLevel: ActiveLevel) -> None:
        """
        Initialisation method.
        Parameters:
            log : Shared logging object.
            activeLevel : Active level, high or low.
        """

        self.log = log

        # Initialise IO.
        self.ioType = DigtialIoType.DIGITAL_OUTPUT
        self.activeLevel = activeLevel
        self._level = None
        self._active = False

        self.log.debug(f'Instantiated digital output : active level : {self.activeLevel}')

    @property
    def active(self) -> None:
        """
        Getter property for output state (active or not).
        This whether or not the output is in the active condition.
        """

        return self._active

    @property
    def level(self) -> None:
        """
        Getter property for output level (high or low).
        This is the raw value of the output written, not whether the signal is active or not.
        """
        return self._level

    @level.setter
    def level(self, l: Level) -> None:
        """
        Setter property for output level (high or low).
        Level and active condition are related,
        so the active condition will be set here accordingly.
        Parameters:
            l : level to set output to.
        """
        self._level = l

        # Set active condition accordingly.
        # If level is the same as the active state then output is active.
        if l == Level.LOW:
            if self.activeLevel == ActiveLevel.ACTIVE_LOW:
                self._active = True
            else:
                self._active = False
        else:
            if self.activeLevel == ActiveLevel.ACTIVE_LOW:
                self._active = False
            else:
                self._active = True

    @abstractmethod
    def writeDigitalOuputLevel(self) -> None:
        """
        Abstract method to write Level to the digital output.
        This method must be overriden by specific controller class.
        """

        pass
