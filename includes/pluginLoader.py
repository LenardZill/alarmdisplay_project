#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import imp
import os

from ConfigParser import NoOptionError
from includes import globals


def loadplugins():
    try:
        logging.debug('loading plugins')
        for i in getplugins():
            try:
                plugin = loadplugin(i)
            except:
                logging.error('error loading plugin: %s', i['name'])
                logging.debug('error loading plugin: %s', i['name'], exc_info=True)
                pass
            else:
                try:
                    logging.debug('call %s.onload()', i['name'])
                    plugin.onload()
                    globals.pluginList[i['name']] = plugin
                except:
                    logging.error('error calling %s.onload()', i['name'])
                    logging.debug('error calling %s.onload()', exc_info=True)
                    pass
    except:
        logging.error('cannot load plugins')
        logging.debug('cannot load plugins', exc_info=True)
        raise


def getplugins():
    try:
        logging.debug('Search in plugin folder')
        pluginfolder = globals.script_path+'/plugins'
        plugins = []
        for i in os.listdir(pluginfolder):
            location = os.path.join(pluginfolder, i)
            if not os.path.isdir(location) or not i + '.py' in os.listdir(location):
                continue
            try:
                if globals.config.getint('Plugins', i):
                    info = imp.find_module(i, [location])
                    plugins.append({'name': i, 'info': info})
                    logging.debug('Plugin [ENABLED ] %s', i)
                else:
                    logging.debug('Plugin [DISABLED] %s ', i)
            except NoOptionError:
                logging.warning('Plugin [NO CONF ] %s', i)
                pass
    except:
        logging.error('Error during plugin search')
        logging.debug('Error during plugin search', exc_info=True)
        raise
    return plugins


def loadplugin(plugin):
    try:
        logging.debug('load plugin: %s', plugin['name'])
        return imp.load_module(plugin['name'], *plugin['info'])
    except:
        logging.error('cannot load plugin: %s', plugin['name'])
        logging.debug('cannot load plugin: %s', plugin['name'], exc_info=True)
        raise
