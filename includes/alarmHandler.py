#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

from includes import globals


def processalarm(typ, freq, data):
    try:
        logging.debug('[    ALARM    ]')
        for pluginName, plugin in globals.pluginList.items():

            if globals.config.getint("Alarmdisplay","useRegExFilter"):
                from includes import filter
                if filter.checkFilters(typ,data,pluginName,freq):
                    logging.debug("call Plugin: %s", pluginName)
                    try:
                        plugin.run(typ,freq,data)
                        logging.debug("return from: %s", pluginName)
                    except:
                        pass
            else:
                logging.debug("call Plugin: %s", pluginName)
                try:
					plugin.run(typ,freq,data)
					logging.debug("return from: %s", pluginName)
                except:
					# call next plugin, if one has thrown an exception
					pass
        logging.debug('[END ALARM]')
    except:
        logging.exception('Error in alarm processing')
