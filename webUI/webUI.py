import re
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
import grpc
import webUI.ui_pb2 as ui_pb2
import webUI.ui_pb2_grpc as ui_pb2_grpc

from flask import current_app
from webUI.auth import login_required
from webUI.db import get_db

from generic.genericConstants import *

bp = Blueprint('webUI', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Index (start) page for webUI.
    """

    # Initialise web page refresh rate to slow.
    # If connected to a controller then can speed up.
    updatePeriod = current_app.config["UI_REFRESH_PERIOD_SLOW"]

    # Initialise flag for stale data,
    # i.e. if no or failed status response from controller.
    staleData = True
    cntrlData = {}

    # If request is POST then check for button press or control.
    if request.method == 'POST':
        # Check for controller mode changes.
        reqMode = ""
        if request.form.get('MODEON') == ControllerMode.ON.name:
            reqMode = ControllerMode.ON.name
        elif request.form.get('MODEOFF') == ControllerMode.OFF.name:
            reqMode = ControllerMode.OFF.name
        elif request.form.get('MODEAUTO') == ControllerMode.AUTO.name:
            reqMode = ControllerMode.AUTO.name
        elif request.form.get('MODEMANUAL') == ControllerMode.MANUAL.name:
            reqMode = ControllerMode.MANUAL.name

        # Set refresh rate to no delay.
        # Will change after next GET when set slow/fast.
        updatePeriod = 0

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
                pass
            else:
                # Status was not good, so need to display an error to the user.
                # Set an error string that can be displayed on the UI.
                if response.status == ui_pb2.UiModeStatus.CS_MODE_FAIL:
                    if response.reason == ControllerModeReason.NOT_ACTIVE.name:
                        error = "Controller must be in ACTIVE state to change mode."
                        print(error)
                    elif response.reason == ControllerModeReason.NO_CHANGE.name:
                        error = "Attempting to change to current mode."                       
                        print(error)

        except grpc.RpcError as e:
            # Failed to receive response from server.
            pass
            print("Server exception...")

        return render_template('webUI/index.html', refresh=0, linkStale=staleData, cData=cntrlData)

    # If not POST then GET current page.
    else:
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
                    "program" : response.program,
                    "outputs" : response.outputs
                }

                # Speed up web page refresh rate now that we are connected.
                updatePeriod = current_app.config["UI_REFRESH_PERIOD_FAST"]

        except grpc.RpcError as e:
            # Failed to receive response from server.
            pass

        return render_template('webUI/index.html', refresh=updatePeriod, linkStale=staleData, cData=cntrlData)
