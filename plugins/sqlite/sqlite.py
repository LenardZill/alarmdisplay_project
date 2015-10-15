#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import sqlite3

from includes import globals
from includes.helper import alarmHelper


def onload():
    try:
        pass
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
        raise


def run(typ, freq, data):
    try:
        try:
            logging.debug('connect to sqlite')
            connection = sqlite3.connect(globals.config.get('sqlite', 'dbpath'))
            connection.text_factory = str
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS ' + globals.config.get('sqlite', 'dbtable') +
                           '(ric TEXT, function TEXT, message TEXT)')
            connection.commit()
        except:
            logging.error('cannot connect to sqlite')
            logging.debug('cannot connect to sqlite', exc_info=True)
        else:
            try:
                logging.debug('Insert POC')
                cursor.execute('INSERT INTO ' + globals.config.get('sqlite', 'dbtable') +
                                ' VALUES(?,?,?)', (data['ric'], data['function'], data['msg']))
                connection.commit()
            except:
                logging.error('cannot insert POC')
                logging.debug('cannot insert POC', exc_info=True)
                return
        finally:
            logging.debug('close sqlite')
            try:
                cursor.close()
                connection.close()
            except:
                pass
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
