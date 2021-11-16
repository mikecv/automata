#!/usr/bin/env python3

from datetime import datetime
import logging
import json

import grpc
import sprinklers.ui_pb2 as ui_pb2
import sprinklers.ui_pb2_grpc as ui_pb2_grpc

from sprinklers.config import *
from sprinklers.controller import *


class UiCommands(ui_pb2_grpc.UiMessages):
    """
    GRPC UiMessages messaging class.
    """

    def __init__(self, config: Config, log: logging, ctrl: SprinklerController) -> None:
        """
        Initialisation method.
        Parameters:
            config : Mainline configuration object.
            ctrl : Controller object.
        """

        self.cfg = config
        self.log = log
        self.ctrl = ctrl

    def GetControllerStatus(self, request, context):
        """
        Respond to controller status request from UI.
        """

        if request.cmd == ui_pb2.UiCmd.U_CNTRL_STATUS:
            try:
                # Respond to the UI.
                resp = ui_pb2.ControllerStatusResp()
                resp.status = ui_pb2.StatusCmdStatus.US_GOOD
                resp.name = self.cfg.ControllerName
                resp.state = self.ctrl.state.name
                # Show day of the week in controller time, so that user can compare with program.
                resp.cTime = datetime.now().strftime("%A, %d/%m/%Y, %H:%M:%S")
                resp.mode = self.ctrl.mode.name
                # Serialise controller data - inputs, outputs, controller program.
                resp.program = self.programSerialised()
                resp.inputs = self.inputsSerialised()
                resp.outputs = self.outputsSerialised()
                return resp

            except grpc.RpcError as e:
                # Server-side GRPC error.
                context.set_code(ui_pb2.StatusCmdStatus.US_SERVER_EXCEPTION)
                context.set_details(f"Server exception, status : {e.code()}; details : {e.details()}")
                self.log.error(f'Server exception, status : {e.code()}; details : {e.details()}')
                return ui_pb2.ui_pb2.ControllerStatusResp()
        else:
            # Unexpected command in controller status request.
            context.set_code(ui_pb2.StatusCmdStatus.US_UNEXPECTED_CMD)
            context.set_details("Unexpected command.")
            self.log.error(f'Unexpected command from UI : {request.cmd}')
            return ui_pb2.ui_pb2.ControllerStatusResp()

    def SetControllerMode(self, request, context):
        """
        Respond to controller mode set request from UI.
        """

        if request.cmd == ui_pb2.UiModeControl.C_SET_MODE:
            try:
                # Need to set the mode to the requested value (if possible).
                setStatus, setReason = self.ctrl.setMode(ControllerMode[f'{request.reqMode}'])

                # Respond to the UI.
                # If successful mode is changed, reason code is blank.
                resp = ui_pb2.SetControllerModeResp()
                resp.status = setStatus
                resp.setMode = self.ctrl.mode.name
                resp.reason = setReason.name
                return resp

            except grpc.RpcError as e:
                # Server-side GRPC error.
                context.set_code(ui_pb2.UiModeStatus.CS_SERVER_EXCEPTION)
                context.set_details(f"Server exception, status : {e.code()}; details : {e.details()}")
                self.log.error(f'Server exception, status : {e.code()}; details : {e.details()}')
                return ui_pb2.ui_pb2.SetControllerModeResp()
        else:
            # Unexpected command in controller mode set request.
            context.set_code(ui_pb2.UiModeStatus.CS_UNEXPECTED_CMD)
            context.set_details("Unexpected command.")
            self.log.error(f'Unexpected command from UI : {request.cmd}')
            return ui_pb2.ui_pb2.SetControllerModeResp()

    def inputsSerialised(self) -> str:
        """
        Get inputs and put into a dictionary,
        and then convert to json string.
        Serialising to send to UI if requested.
        Returns:
            serialised dictionary of input IO.
        """

        ins = []
        # Serialise all the inputs.
        for di in self.ctrl.digitalInputs:
            iData = {
                "iName" : di.inputName,
                "iActive" : di.active
            }
            ins.append(iData)
        # Complete dictionaty with header and inputs.
        iDict = {
            "gName" : self.ctrl.inputsGroupName,
            "inputs" : ins
        }

        return json.dumps(iDict)

    def outputsSerialised(self) -> str:
        """
        Get outputs and put into a dictionary,
        and then convert to json string.
        Serialising to send to UI if requested.
        Returns:
            serialised dictionary of output IO.
        """

        outs = []
        # Serialise all the outputs.
        for do in self.ctrl.digitalOutputs:
            oData = {
                "oName" : do.outputName,
                "oActive" : do.active
            }
            outs.append(oData)
        # Complete dictionaty with header and outputs.
        oDict = {
            "gName" : self.ctrl.outputsGroupName,
            "outputs" : outs
        }

        return json.dumps(oDict)

    def programSerialised(self) -> str:
        """
        Get controller program and convert to json string.
        Serialising to send to UI if requested.
        Returns:
            serialised dictionary of controller program data.
        """

        myDays = []
        for d in self.ctrl.program["MyDays"]:
            # Only send day name to UI.
            myDays.append(d.name)
        pgs = []
        for p in self.ctrl.program["Programs"]:
            pgs.append(p)
        pDict = {
            "MyDays" : myDays,
            "Programs" : pgs
        }

        print(json.dumps(pDict))
        return json.dumps(pDict)
