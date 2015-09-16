#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

from includes import globals


def processalarm(typ, freq, data):
    try:
        logging.debug('[    ALARM    ]')
        for pluginName, plugin in globals.pluginList.items():
            logging.debug('call Plugin: %s', pluginName)
            try:
                plugin.run(typ, freq, data)
                logging.debug('return from: %s', pluginName)
            except:
                pass
        logging.debug('[END ALARM]')
    except:
        logging.exception('Error in alarm processing')
