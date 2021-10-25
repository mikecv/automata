#!/usr/bin/env python3

import logging

from generic.genericIO import *
from sprinklers.config import *

class DigitalInput(GenericIO):   
    """
    Class to represent a controller digital input.
    Derive from a generic input/output (IO) class.
    """

    def __init__(self, log: logging, activeState: ActiveState) -> None:
        """
        Initialisation method.
        Parameters:
            log : Mainline logging object.
            activeState : Active state, high or low.
        """

        self.log = log

        # Super class initialisations.
        # Initialise input type to digital input.
        GenericIO.__init__(self, log, IOType.DIGITAL_INPUT, activeState)
