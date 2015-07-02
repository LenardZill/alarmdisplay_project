#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

from includes import globals

def processAlarm(typ,freq,data):
    try:
        logging.debug('[    ALARM    ]')
        for pluginName, plugin in globals.pluginList.items():
            logging.debug('call plugins: %s', pluginName)
            plugin.run(typ,freq,data)
            logging.debug('return from: %s', pluginName)
        logging.debug("[    END ALARM    ]")
    except:
        logging.exception('Error in Alarm processing')