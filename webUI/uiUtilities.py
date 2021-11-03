#!/usr/bin/env python3

from typing import Tuple

from flask import flash
import grpc
import json

import webUI.ui_pb2 as ui_pb2
import webUI.ui_pb2_grpc as ui_pb2_grpc

from flask import current_app

from generic.genericConstants import *

def setControllerMode(reqMode: str) -> Tuple[bool, bool]:
    """
    Set the controller mode.
    Parameters:
        reqMode : Mode to set the controller to.
    Returns:
        staleData : Flag if controller responded or not
        isError : Flag indicating if there is an alert to display.
    """

    # Initialise flag for stale data,
    staleData = True

    # Initialise error flag,
    isError = False

    # Set up channel to controller to get interface with controller.
    channel = grpc.insecure_channel(f'{current_app.config["UI_IP"]}:{current_app.config["UI_PORT"]}')
    stub = ui_pb2_grpc.UiControlModeStub(channel)

    # Construct controller status request message object.
    setModeCmd = ui_pb2.SetControllerModeCmd()
    setModeCmd.cmd = ui_pb2.UiModeControl.C_SET_MODE
    setModeCmd.reqMode = reqMode

    try:
        # Send mode command to the server.
        response = stub.SetControllerMode(setModeCmd)

        if response.status == ui_pb2.UiModeStatus.CS_GOOD:
            # Status response is good, so nothing to do.
            # Status will be updated next time GET refreshed.
            staleData = False
        else:
            # Status was not good, so need to display an error to the user.
            if response.status == ui_pb2.UiModeStatus.CS_MODE_FAIL:
                staleData = False
                isError = True
                if response.reason == ControllerModeReason.NOT_ACTIVE.name:
                    flash('Controller must be in ACTIVE state to change mode.', 'error')
                elif response.reason == ControllerModeReason.NO_CHANGE.name:
                    flash('Attempting to change to current mode.', 'warning')

    except grpc.RpcError as e:
        # Failed to receive response from server.
        pass

    return staleData, isError

def getControllerStatus() -> Tuple[bool, dict, dict, dict, int]:
    """
    Get the controller status.
    Returns:
        staleData : Flag if controller responded or not
        cntrlData : Controller status data.
        inputData : Controller input dacntrlDatata.
        outputData : Controller outputs dacntrlDatata.
        updatePeriod : UI update / refresh period.
    """

    # Initialise web page refresh rate to slow.
    updatePeriod = current_app.config["UI_REFRESH_PERIOD_SLOW"]

    # Initialise flag for stale data,
    staleData = True

    #Initialise controller and input data.
    cntrlData = {}
    inputData = {}
    outputData = {}

    # Set up channel to controller to get interface with controller.
    channel = grpc.insecure_channel(f'{current_app.config["UI_IP"]}:{current_app.config["UI_PORT"]}')
    stub = ui_pb2_grpc.UiMessagesStub(channel)

    # Construct controller status request message object.
    getStatusCmd = ui_pb2.ControllerStatusCmd()
    getStatusCmd.cmd = ui_pb2.UiCmd.U_CNTRL_STATUS

    # Initialise web page refresh rate to slow.
    # If connected to a controller then can speed up.
    updatePeriod = current_app.config["UI_REFRESH_PERIOD_SLOW"]
    try:
        # Send status request command to the server.
        response = stub.GetControllerStatus(getStatusCmd)

        if response.status == ui_pb2.StatusCmdStatus.US_GOOD:
            # Status response good, so update controller status object.
            staleData = False
            cntrlData = {
                "name" : response.name,
                "state" : response.state,
                "cTime" : response.cTime,
                "mode" : response.mode,
                "program" : response.program
            }
            inputData = json.loads(response.inputs)
            outputData = json.loads(response.outputs)

            # Speed up web page refresh rate now that we are connected.
            updatePeriod = current_app.config["UI_REFRESH_PERIOD_FAST"]
        else:
            # Failed to get good status from controller.
            print("Failed to get good status from controller.")

    except grpc.RpcError as e:
        # Failed to receive response from server.
        pass

    return staleData, cntrlData, inputData, outputData, updatePeriod
