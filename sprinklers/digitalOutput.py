#!/usr/bin/env python3

import logging

from generic.genericDigitalOutput import *
from sprinklers.config import *

class DigitalOutput(GenericDigitalOutput):   
    """
    Class to represent a controller digital output.
    Derive from a generic digital IO class.
    """

    def __init__(self, log: logging, outputName: str, activeLevel: ActiveLevel) -> None:
        """
        Initialisation method.
        Parameters:
            log : Mainline logging object.
            outputName : Name for this output.
            activeLevel : Active level, high or low.
        """

        self.log = log

        # Super class initialisations.
        # Initialise digital output with active level.
        GenericDigitalOutput.__init__(self, log, activeLevel)

        # Initialise specific class variables.
        self.outputName = outputName

        self.log.debug(f'Instantiated digital output with name : {outputName}')

    def writeDigitalOuputLevel(self, oLevel: Level) -> None:
        """
        Write digital output.
        Parameters:
            oLevel : Level (Hi or Low) to set output to.
        """

        # This is at the hardware layer so writing level.
        self.level = oLevel
