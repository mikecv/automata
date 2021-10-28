#!/usr/bin/env python3

import logging

from generic.genericDigitalInput import *
from sprinklers.config import *

class DigitalInput(GenericDigitalInput):   
    """
    Class to represent a controller digital input.
    Derive from a generic input class.
    """

    def __init__(self, log: logging, inputName: str, activeState: ActiveState) -> None:
        """
        Initialisation method.
        Parameters:
            log : Mainline logging object.
            inputName : Name for this input.
            activeState : Active state, high or low.
        """

        self.log = log

        # Super class initialisations.
        # Initialise digital input with active state.
        GenericDigitalInput.__init__(self, log, activeState)

        # Initialise specific class variables.
        self.inputName = inputName

    def readDigitalInput(self) -> None:
        """
        Definition of abstract method to read digital input.
        """

        # <TODO>
        self.level = Level.LOW
