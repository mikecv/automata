#!/usr/bin/env python3

from abc import ABC, abstractmethod

from generic.genericConstants import *


class GenericController():   
    """
    Class to represent a generic controller.
    """

    def __init__(self, name) -> None:
        """
        Initialisation method.
        """

        self.ctrlName = name

        # Initialise state of the controller.
        self.stayAlive = True
        self.state = ControllerState.STARTING

    def stateMachine(self) -> None:
        """
        State machine method.
        Performs state transitions and invokes methods as required.
        """

        if self.state == ControllerState.STARTING:
            self.state = ControllerState.INITIALISING
        elif self.state == ControllerState.INITIALISING:
            self.initialise()
        elif self.state == ControllerState.ACTIVE:
            self.controlling()
        elif self.state == ControllerState.TERMINATING:
            self.stayAlive = False

    def initialise(self) -> None:
        """
        Initialise class variables and state.
        """

        # Initialise stay alive flag.
        self.stayAlive = True

        # Transition to the active state.
        self.state = ControllerState.ACTIVE

    @abstractmethod
    def controlling(self) -> None:
        """
        Abstract method to perform controlling functions.
        This method must be overriden by specific controller class.
        """

        pass