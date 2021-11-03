#!/usr/bin/env python3

import logging
import random

from generic.genericDigitalInput import *
from sprinklers.config import *

class DigitalInput(GenericDigitalInput):   
    """
    Class to represent a controller digital input.
    Derive from a generic digital IO class.
    """

    def __init__(self, log: logging, inputName: str, activeLevel: ActiveLevel) -> None:
        """
        Initialisation method.
        Parameters:
            log : Mainline logging object.
            inputName : Name for this input.
            activeLevel : Active state, high or low.
        """

        self.log = log

        # Super class initialisations.
        # Initialise digital input with active condition.
        GenericDigitalInput.__init__(self, log, activeLevel)

        # Initialise specific class variables.
        self.inputName = inputName

        self.log.debug(f'Instantiated digital input with name : {self.inputName}')

    def readDigitalInputLevel(self) -> None:
        """
        Read digital input.
        """

        # This is at the hardware layer so reading if input is low or high,
        # and then setting the active (or not) condition that this corresponds to.
        # Note that only reading and setting the level here; the active 
        # condition will be set by the base class.

        # <TODO> this will be reading input level from hardware.
        # <TODO> For now set the input to a random value.

        self.level = random.choice(list(Level))
