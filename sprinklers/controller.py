#!/usr/bin/env python3

from threading import Thread
import logging
import time
import json
import random

from generic.genericController import *
from sprinklers.digitalInput import *
from sprinklers.digitalOutput import *
from sprinklers.config import *

class SprinklerController(GenericController, Thread):   
    """
    Class to represent a sprinkler controller.
    Derive from a generic controller class.
    """

    def __init__(self, config: Config, log: logging, name: str, iFile: str, oFile: str) -> None:
        """
        Initialisation method.
        Parameters:
            config : Mainline configuration object.
            log : Mainline logging object.
            name : Name of the controller.
            iFile : Name of inputs configuration (json) file.
            oFile : Name of outputs configuration (json) file.
        """

        self.cfg = config
        self.log = log

        # Super class initialisations.
        GenericController.__init__(self, name, log)
        Thread.__init__(self)

        # Import the inputs (IO) configuration file.
        # Some of the configuration data is generic IO and some is specific to this implementation.
        # The arrays of digital IO is initialised in the generic classes.
        try:
            with open(iFile) as inputsConfig:
                ic = json.load(inputsConfig)

                # Import the group name for the inputs.
                self.inputsGroupName = ic["GroupName"]
                self.log.debug(f'Importing inputs with group name : {self.inputsGroupName}')
                # Go through all the inputs in the config file.
                # Create the digital inputs instance and add to list.
                for i in ic["IO"]:
                    inputName = i["Name"]
                    inputActiveLevel = ActiveLevel[i["activeLevel"]]
                    self.digitalInputs.append(DigitalInput(self.log, inputName, inputActiveLevel))
                    self.log.debug(f'Importing input name : {inputName}; active level : {inputActiveLevel}')
        except Exception:
            # Failed to import inputs configuration file.
            self.log.error(f'Failed to import inputs configuration file.')

        # Import the outputs (IO) configuration file.
        # Some of the configuration data is generic IO and some is specific to this implementation.
        # The arrays of digital IO is initialised in the generic classes.
        try:
            with open(oFile) as outputsConfig:
                oc = json.load(outputsConfig)

                # Import the group name for the outputs.
                self.outputsGroupName = oc["GroupName"]
                self.log.debug(f'Importing outputs with group name : {self.outputsGroupName}')
                # Go through all the outputs in the config file.
                # Create the digital outputs instance and add to list.
                for o in oc["IO"]:
                    outputName = o["Name"]
                    outputActiveLevel = ActiveLevel[o["activeLevel"]]
                    digOut = DigitalOutput(self.log, outputName, outputActiveLevel)
                    self.digitalOutputs.append(digOut)
                    self.log.debug(f'Importing output name : {outputName}; active level : {outputActiveLevel}')

                    # Set initial output state.
                    digOut.level = Level[o["InitLevel"]]

        except Exception:
            # Failed to import outputs configuration file.
            self.log.error(f'Failed to import outputs configuration file.')

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

        # Initialise variable to follow if still can control.
        # If canControl set to False because of error, controlling will end,
        # and will return to run method and state machine.
        canControl = True

        while canControl:

            # All the period activities that the controller has to do.

            # Read the state of all the inputs.
            for i in self.digitalInputs:
                i.readDigitalInputLevel()

            # Look at the programs to see if any action needs to be taken.
            # <TODO> Look through programs for actions to take, i.e. outputs to assert.
            # For now just set outputs to random values to exercise the UI.
            for o in self.digitalOutputs:
                o.writeDigitalOuputLevel(random.choice(list(Level)))

            # Wait a bit before trying again later.
            time.sleep(self.cfg.Timers["ControllerSleep"])