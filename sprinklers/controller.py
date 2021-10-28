#!/usr/bin/env python3

from threading import Thread
import logging
import time
import json

from generic.genericController import *
from sprinklers.digitalInput import *
from sprinklers.config import *

class SprinklerController(GenericController, Thread):   
    """
    Class to represent a sprinkler controller.
    Derive from a generic controller class.
    """

    def __init__(self, config: Config, log: logging, name: str, iFile: str) -> None:
        """
        Initialisation method.
        Parameters:
            config : Mainline configuration object.
            log : Mainline logging object.
            name : Name of the controller.
            iFile : Name of inputs configuration (json) file.
        """

        self.cfg = config
        self.log = log

        # Super class initialisations.
        GenericController.__init__(self, name, log)
        Thread.__init__(self)

        # Import the inputs (IO) configuration file.
        # Some of the configuration data is generic IO and some is specific to this implementation.
        self.digitalInputs = []
        try:
            with open(iFile) as inputsConfig:
                ic = json.load(inputsConfig)

                # Import the group name for the inputs.
                self.groupName = ic["GroupName"]
                self.log.debug(f'Importing inputs with group name : {self.groupName}')
                # Go through all the inputs in the config file.
                # Create the digital inputs instance and add to list.
                for i in ic["Inputs"]:
                    inputName = i["Name"]
                    inputValidState = i["ValidState"]
                    self.digitalInputs.append(DigitalInput(self.log, inputName, inputValidState))
                    self.log.debug(f'Importing input name : {inputName}; valid state : {inputValidState}')
        except Exception:
            # Failed to import inputs configuration file.
            self.log.error(f'Failed to import inputs configuration file.')

    def run(self) -> None:
        """
        Run threaded method.
        Loop forever, checking for state transitions.
        Mainline will kill thread when self.stayAlive is False.
        """

        self.log.debug(f'Controller thread running.')

        while self.stayAlive:
            # Check state in state machine.
            self.stateMachine()

    def controlling(self) -> None:
        """
        Definition of abstract method to perform controlling functions.
        """

        self.log.debug(f'Controller processing in ACTIVE mode.')

        while True:

            # <TODO>
            time.sleep(self.cfg.Timers["MainSleep"])