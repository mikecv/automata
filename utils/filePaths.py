#!/usr/bin/env python3

import os

def chkPath(fullPath: str) -> None:
    """
    Given full path and filename check if path exists.
    Create path it doesn't exist.
    Parameters:
        fullPath : Full path and filename to check.
    """

    # Check if path already exist.
    p = os.path.split(fullPath)
    exists = os.path.exists(p[0])
    # If not then create it.
    if exists == False:
        try:
            os.makedirs(p[0])
        except:
            print("Failed to create requested path.")