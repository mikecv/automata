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

    def __init__(self, config: Config, log: logging, name: str, iFile: str, oFile: str, pFile: str) -> None:
        """
        Initialisation method.
        Parameters:
            config : Mainline configuration object.
            log : Mainline logging object.
            name : Name of the controller.
            iFile : Name of inputs configuration (json) file.
            oFile : Name of outputs configuration (json) file.
            pFile : Name of controller program configuration (json) file.
        """

        self.cfg = config
        self.log = log

        # Super class initialisations.
        GenericController.__init__(self, name, log)
        Thread.__init__(self)

        # Import the inputs (IO) configuration file.
        self.importDigitalInputs(iFile)

        # Import the outputs (IO) configuration file.
        self.importDigitalOutputs(oFile)

        # Import the controller program configuration file.
        self.importControllerProgram(pFile)

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

            # All the periodic activities that the controller has to do.

            # Read the state of all the inputs.
            for i in self.digitalInputs:
                i.readDigitalInputLevel()

            # Look at the programs to see if any action needs to be taken.
            # <TODO> Look through programs for actions to take, i.e. outputs to assert.
            # For now just set random output active.
            opChoice = random.choice(range(0, len(self.digitalOutputs), 1))

            self.setAllOutputsInactive()
            if opChoice > 0:
                self.setOutputActive(opChoice)

            # Wait a bit before trying again later.
            time.sleep(self.cfg.Timers["ControllerSleep"])

    def setAllOutputsInactive(self) -> None:
        """
        Set all digital outputs to inactive.
        """

        for o in self.digitalOutputs:
            o.setDigitalOuputActive(False)

        self.log.debug(f'Setting all digital outputs to INACTIVE.')


    def setOutputActive(self, oIdx: int) -> None:
        """
        Set particular outputs to active.
        Also sets the master to active as well.
        Parameters:
            oIdx : Number of digital output (1 onwards)
        """

        self.digitalOutputs[0].setDigitalOuputActive(True)
        self.digitalOutputs[oIdx].setDigitalOuputActive(True)

    def importDigitalInputs(self, iFile: str) -> None:
        """
        Import digital inputs configuration file.
        Parameters:
            iFile : Name of digital inputs configuration file.
        """

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
                for i in ic["Inputs"]:
                    inputName = i["Name"]
                    # <TODO> Add checks that active level in config is a valid value.
                    inputActiveLevel = ActiveLevel[i["activeLevel"]]
                    self.digitalInputs.append(DigitalInput(self.log, inputName, inputActiveLevel))
                    self.log.debug(f'Importing input name : {inputName}; active level : {inputActiveLevel}')
        except Exception:
            # Failed to import inputs configuration file.
            self.log.error(f'Failed to import inputs configuration file.')

    def importDigitalOutputs(self, oFile: str) -> None:
        """
        Import digital outputs configuration file.
        Parameters:
            oFile : Name of digital outputs configuration file.
        """

        # Import the outputs (IO) configuration file.
        # Some of the configuration data is generic IO and some is specific to this implementation.
        # The arrays of digital IO is initialised in the generic classes.
        try:
            with open(oFile) as outputsConfig:
                oc = json.load(outputsConfig)

                # Import the group name for the outputs.
                self.outputsGroupName = oc["GroupName"]
                self.log.debug(f'Importing outputs with group name : {self.outputsGroupName}')

                # Get the master output, this will be digitial output 0.
                outputName = oc["Master"]["Name"]
                outputActiveLevel = ActiveLevel[oc["Master"]["activeLevel"]]
                digOut = DigitalOutput(self.log, outputName, outputActiveLevel)
                self.digitalOutputs.append(digOut)
                self.log.debug(f'Importing MASTER output name : {outputName}; active level : {outputActiveLevel}')

                # Go through all the (non-master) outputs in the config file.
                # Create the digital outputs instance and add to list.
                for o in oc["Outputs"]:
                    outputName = o["Name"]
                    # <TODO> Add checks that active level in config is a valid value.
                    outputActiveLevel = ActiveLevel[o["activeLevel"]]
                    digOut = DigitalOutput(self.log, outputName, outputActiveLevel)
                    self.digitalOutputs.append(digOut)
                    self.log.debug(f'Importing output name : {outputName}; active level : {outputActiveLevel}')

                    # Set initial output state.
                    digOut.level = Level[o["InitLevel"]]

        except Exception:
            # Failed to import outputs configuration file.
            self.log.error(f'Failed to import outputs configuration file.')

    def importControllerProgram(self, pFile: str) -> None:
        """
        Import controller program configuration file.
        Perform consistency and feasibility check on data, e.g. that
        programs are achievable, days/times exist etc.
        Parameters:
            pFile : Name of controller program configuration file.
        """

        # Import the controller program configuration file.
        self.log.debug(f'Importing controller programs.')
        try:
            with open(pFile) as programConfig:
                pc = json.load(programConfig)

                # Import the group name for the outputs.
                myDays = []
                # Get the allocated days for the controller.
                # <TODO> Add checks that days are legitimate days.
                for day in pc["MyDays"]:
                    myDays.append(ProgramDays[day])
                # Import each of the programs.
                pgs = []
                for p in pc["Programs"]:
                    pg = {}
                    progName = p["Name"]
                    # <TODO> Add checks that start times and durations are valid,
                    # would result in the cycke starting and ending in the same day.
                    for ot in p["OnTimes"]:
                        startTime = ot["Start"]
                        duration = ot["Duration"]
                        stations = []
                        for st in ot["Stations"]:
                            stations.append(st)
                        ots = {"Start": startTime, "Duration": duration, "Stations": stations}
                    pg = {"Name": progName, "OnTimes": ots}
                    pgs.append(pg)
                self.program = {"MyDays": myDays, "Programs": pgs}

        except Exception:
            # Failed to import controller program configuration file.
            self.log.error(f'Failed to import controller program configuration file.')
