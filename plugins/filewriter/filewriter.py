#!/usr/bin/python
# -*- coding: cp1252 -*-
from datetime import datetime
import logging
from includes import globals

def onload():
    try:
        pass
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
        raise


def run(typ, freq, data):
    try:
        logging.debug(data)
        f = open(globals.config.get('filewriter', 'path'), 'w')
        f.write(data['alarmid'] + ';' +
                data['ric'] + ';' +
                datetime.strftime(data['date'], '%d.%m.%Y %H:%M:%S') + ';' +
                data['description'] + ';' +
                data['keyword_org'] + ';' +
                data['keyword'] + ';' +
                data['msg_trimmed'] + ';' +
                data['info'] + ';' +
                data['firestations'] + ';' +
                data['msg'] + ';' +
                '\n')
        f.close()
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
