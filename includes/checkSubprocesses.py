#!/usr/bin/python
# -*- coding: cp1252 -*-
#
"""
Functions for checking the subprocesses rtl_fm and multimon-ng
Used in boswatch.py at startup and designated for watching-service

@author:         Jens Herrmann
"""

import logging

from includes import globals


def checkRTL():
    try:
        rtlLog = open(globals.log_path+"rtl_fm.log","r").read()
        if ("exiting" in rtlLog) or  ("Failed to open" in rtlLog):
            logging.debug("\n%s", rtlLog)
            raise OSError("starting rtl_fm returns an error")
    except OSError:
        raise
    except:
        logging.critical("cannot check rtl_fm.log")
        logging.debug("cannot check rtl_fm.log", exc_info=True)
        raise

def checkMultimon():
    try:
        multimonLog = open(globals.log_path+"multimon.log","r").read()
        if ("invalid" in multimonLog) or ("error" in multimonLog):
            logging.debug("\n%s", multimonLog)
            raise OSError("starting multimon-ng returns an error")
    except OSError:
        raise
    except:
        logging.critical("cannot check multimon.log")
        logging.debug("cannot check multimon.log", exc_info=True)
        raise