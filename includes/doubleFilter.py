#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Created on 16.09.2015

@author: LZill
'''

import logging
import time

from includes import globals

def checkID(typ, id, msg=""):
    timestamp = int(time.time())

    for i in range(len(globals.doubleList)):
        (xID, xTimestamp, xMsg) = globals.doubleList[i]
        if id == xID and timestamp < xTimestamp + globals.config.getint("Alarmdisplay", "doubleFilter_ignore_time"):
            if "POC" in typ and globals.config.getint("Alarmdisplay", "doubleFilter_check_msg"):
                if msg in xMsg:
                    logging.info("%s double alarm (id+msg): %s within %s second(s)", typ, xID, timestamp-xTimestamp)
                    return False
            else:
                logging.info("%s double alarm (id): %s within %s second(s)", typ, xID, timestamp-xTimestamp)
                return False
    return True


def newEntry(id, msg = ""):
    timestamp = int(time.time())
    globals.doubleList.append((id, timestamp, msg))

    logging.debug("Added %s to doubleList", id)

    if len(globals.doubleList) > globals.config.getint("Alarmdisplay", "doubleFilter_ignore_entries"):
        globals.doubleList.pop(0)
