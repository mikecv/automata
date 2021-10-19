#!/usr/bin/env python3

from concurrent import futures
from threading import Thread
import time
import grpc
import sprinklers.ui_pb2_grpc as ui_pb2_grpc

from sprinklers.constants import *
from sprinklers.uiMessages import *


class UIServer(Thread):   
    """
    Class to present a UI server for controller data.
    Derive from Thread class.
    """

    def __init__(self, config: Config, log, ctrl: SprinklerController) -> None:
        """
        Initialisation method.
        Parameters:
            config : Mainline configuration object.
            log : Mainline logging object.
            controller : Controller object to report on.
        """

        Thread.__init__(self)
        self.cfg = config
        self.log = log
        self.ctrl = ctrl

        # Initialise state of the controller.
        self.stayAlive = True

    def run(self) -> None:
        """
        Run threaded method.
        Loop forever, checking for ui requests.
        Mainline will kill thread when self.stayAlive is False.
        """

        self.log.debug("Starting UI server...")
        print("Starting UI server...")

        # Configure and start the server to listen for messages from UI.
        # Add servicers for all UI services.
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        ui_pb2_grpc.add_UiMessagesServicer_to_server(UiCommands(self.cfg, self.ctrl), server)
        ui_pb2_grpc.add_UiControlModeServicer_to_server(UiCommands(self.cfg, self.ctrl), server)
        server.add_insecure_port(f'[::]:{self.cfg.UI["UIPort"]}')
        server.start()

        while self.stayAlive:
            time.sleep(self.cfg.UI["UISleep"])

    def stopServingUI(self) -> None:
        """
        Method to stop serving UI data.
        """

        self.stayAlive = False
