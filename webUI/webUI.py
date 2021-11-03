from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flask import current_app
from webUI.auth import login_required
from webUI.db import get_db

from generic.genericConstants import *
from webUI.uiUtilities import *

bp = Blueprint('webUI', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Index (start) page for webUI.
    """

    # If POST then perform any actions, e.g. set controller mode.
    # If controller action was successful then get current controller status before rendering.

    # Initialise update period and controller status data in case no response from controller.
    updatePeriod = current_app.config["UI_REFRESH_PERIOD_SLOW"]
    cntrlData = {}
    inputData = {}
    outputData = {}

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

        # Set message to controller to set the mode.
        staleData, isError = setControllerMode(reqMode)

        # If controller action was successful then get controller status.
        if staleData == False:
            # Get the latest controller data.
            staleData, cntrlData, inputData, outputData, updatePeriod = getControllerStatus()

            # If there was an error when doing the controller action,
            # then overwrite the update / represh period to give more time for the alert.
            if isError == True:
                updatePeriod = current_app.config["UI_REFRESH_PERIOD_SLOW"]

        # Render the web page with controller data,
        # taking into account any action to change modes.
        return render_template('webUI/index.html', refresh=updatePeriod, linkStale=staleData, cData=cntrlData, iData=inputData, oData=outputData)
    else:
        # Request is for a GET so just get controller status.
        # Get the latest controller data.
        staleData, cntrlData, inputData, outputData, updatePeriod = getControllerStatus()

        # Render the web page with controller data,
        # taking into account any action to change modes.
        return render_template('webUI/index.html', refresh=updatePeriod, linkStale=staleData, cData=cntrlData, iData=inputData, oData=outputData)
