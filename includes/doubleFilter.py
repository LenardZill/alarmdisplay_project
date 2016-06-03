#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import time

from includes import globals


def check_id(typ, id, msg=''):
    timestamp = int(time.time())
    for i in range(len(globals.doubleList)):
        (xid, xtimestamp, xmsg) = globals.doubleList[i]
        if id == xid and timestamp < xtimestamp + globals.config.getint('Alarmdisplay', 'doubleFilter_ignore_time'):
            if 'POC' in typ and globals.config.getint('Alarmdisplay', 'doubleFilter_check_msg'):
                if msg in xmsg:
                    logging.info('%s double alarm (id+msg): %s within %s second(s)', typ, xid, timestamp-xtimestamp)
                    return False
            else:
                logging.info('%s double alarm (id): %s within %s second(s)', typ, xid, timestamp-xtimestamp)
                return False
    return True


def new_entry(id, msg=''):
    timestamp = int(time.time())
    globals.doubleList.append((id, timestamp, msg))
    logging.debug('Added %s to doubleList', id)
    if len(globals.doubleList) > globals.config.getint('Alarmdisplay', 'doubleFilter_ignore_entries'):
        globals.doubleList.pop(0)
