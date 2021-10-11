#!/usr/bin/env python3

from threading import Thread
import logging
import time

from ..generic.genericController import *
from config import *

class SprinklerController(GenericController, Thread):   
    """
    Class to represent a sprinkler controller.
    Derive from a generic controller class.
    """

    def __init__(self, config: Config, log: logging, name: str) -> None:
        """
        Initialisation method.
        Parameters:
            config : Mainline configuration object.
            log : Mainline logging object.
            name : Name of the controller.
        """

        # Super class initialisations.
        GenericController.__init__(self, name)
        Thread.__init__(self)

        self.cfg = config
        self.log = log

    def run(self) -> None:
        """
        Run threaded method.
        Loop forever, checking for state transitions.
        Mainline will kill thread when self.stayAlive is False.
        """

        while self.stayAlive:
            # Check state in state machine.
            self.stateMachine()

    def controlling(self) -> None:
        """
        Definition of abstract method to perform controlling functions.
        """

        while True:

            # <TODO>
            time.sleep(self.cfg.Timers["MainSleep"])