#!/usr/bin/env python3

import argparse
import logging
import logging.handlers
import time
import os

from sprinklers.config import *
from sprinklers.controller import *
from sprinklers.uiServer import *
from utils.filePaths import *

# *******************************************
# Program history.
# 0.1   MDC 09/10/2021  Original.
# *******************************************

# *******************************************
# TODO List
#
# Write unit tests.
# Add program/scheduling functionality.
# *******************************************

# Program name, version, and date.
progName = "sprinklers"
progVersion = "0.1"
progDate = "2021"

# Program main.
def main(cFile: str, lFile: str, iFile: str, oFile: str, pFile: str) -> None:
    """
    Controller mainline.
    Parameters:
        cFile : Json configuration file.
        lFile : Program log file.
        iFile : Inputs configuration file.
        oFile : Outputs configuration file.
        pFile : Program (watering) configuration file.
    """

    # Check if paths for config and logs exists and create if not.
    chkPath(cFile)
    chkPath(lFile)
    chkPath(iFile)
    chkPath(oFile)
    chkPath(pFile)

    # Create configuration values class object.
    cfg = Config(cFile)

    # Create logger. Use rotating log files.
    logger = logging.getLogger(progName)
    logger.setLevel(cfg.DebugLevel)
    handler = logging.handlers.RotatingFileHandler(lFile, maxBytes=cfg.LogFileSize, backupCount=cfg.LogBackups)
    handler.setFormatter(logging.Formatter(fmt=f"%(asctime)s.%(msecs)03d [{cfg.ControllerName}] [%(levelname)-8s] %(message)s", datefmt="%Y%m%d-%H:%M:%S", style="%"))
    logging.Formatter.converter = time.localtime
    logger.addHandler(handler)

    # Log program version.
    logger.info(f'Program version : {progVersion}')

    # Create an instance of a controller.
    # Controller is a threaded class so start the thread running.
    logger.info(f'Creating controller, and starting thread : {cfg.ControllerName}')
    c = SprinklerController(cfg, logger, cfg.ControllerName, iFile, oFile, pFile)
    c.start()

    # Create an instance of a UI server.
    # This will present controller data to UIs.
    logger.info(f'Creating UI web server, and starting thread.')
    ui = UIServer(cfg, logger, c)
    ui.start()

    # Keep checking if controller is still alive,
    # if so, keep processing.
    # <TODO> Implement errors and terminations.
    while c.stayAlive:
        pass

    # Controller not alive, so exit.
    logger.info('Controller is dead!')
    exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Sprinkler Controller.")
    parser.add_argument("-c", "--config", help="Json configuration file.")
    parser.add_argument("-l", "--log", help="Log file.")
    parser.add_argument("-i", "--inputs", help="Json inputs configuration file.")
    parser.add_argument("-o", "--outputs", help="Json outputs configuration file.")
    parser.add_argument("-p", "--program", help="Json (watering) program configuration file.")
    parser.add_argument("-v", "--version", help="Program version.", action="store_true")
    args = parser.parse_args()

    # Check if program version requested.
    # Only show version and don't do anything else.
    if args.version:
        print(f"Program version : {progVersion}")
    else:
        # Use default config & log file names if not specified.
        cFile = os.path.join("./config", progName + "." + "json")
        lFile = os.path.join("./logs", progName + "." + "log")
        iFile = os.path.join("./config", "inputs.json")
        oFile = os.path.join("./config", "outputs.json")
        pFile = os.path.join("./config", "program.json")

        # Check for configuration options different to default.
        if args.config:
            cFile = args.config
        if args.log:
            lFile = args.log
        if args.inputs:
            iFile = args.inputs
        if args.outputs:
            oFile = args.outputs
        if args.program:
            pFile = args.program
        main(cFile, lFile, iFile, oFile, pFile)
