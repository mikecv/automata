#!/usr/bin/env python3

from datetime import datetime
import grpc
import sprinklers.ui_pb2 as ui_pb2
import sprinklers.ui_pb2_grpc as ui_pb2_grpc

from sprinklers.config import *
from sprinklers.controller import *


class UiCommands(ui_pb2_grpc.UiMessages):
    """
    GRPC UiMessages messaging class.
    """

    def __init__(self, config: Config, ctrl: SprinklerController) -> None:
        """
        Initialisation method.
        Parameters:
            config : Mainline configuration object.
            log : Mainline logging object.
            ctrl : Controller object.
        """

        self.cfg = config
        self.ctrl = ctrl

    def GetControllerStatus(self, request, context):
        """
        Respond to controller status request from controller.
        """

        if request.cmd == ui_pb2.UiCmd.U_CNTRL_STATUS:
            try:
                # Respond to the UI.
                resp = ui_pb2.ControllerStatusResp()
                resp.status = ui_pb2.StatusCmdStatus.US_GOOD
                resp.name = self.cfg.ControllerName
                resp.state = self.ctrl.state.name
                resp.cTime = datetime.now().strftime("%H:%M:%S")
                return resp

            except grpc.RpcError as e:
                # Server-side GRPC error.
                context.set_code(ui_pb2.StatusCmdStatus.US_SERVER_EXCEPTION)
                context.set_details(f"Server exception, status : {e.code()}; details : {e.details()}")
                return ui_pb2.ui_pb2.ControllerStatusResp()
        else:
            # Unexpected command in controller status request.
            context.set_code(ui_pb2.StatusCmdStatus.US_UNEXPECTED_CMD)
            context.set_details("Unexpected command.")
            return ui_pb2.ui_pb2.ControllerStatusResp()

