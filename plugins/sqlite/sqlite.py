#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
SQLite Plugin to dispatch POCSAG messages to a SQLite database

@author: Lenard Zill
'''

import logging
import sqlite3

from includes import globals

def run(typ,freq,data):
    try:
        try:
            logging.debug('connect to sqlite')
            connection = sqlite3.connect(globals.database_path)
            cursor = connection.cursor()
        except:
            logging.exception('cannot connect to sqlite')
        else:
            try:
                logging.debug('insert data')
                cursor.execute('INSERT INTO ' + globals.database_table + ' VALUES("%s","%s","%s")', (data['ric'], data['function'], data['msg']))
            except:
                logging.exception('cannot insert data')
    
        finally:
            logging.debug('close sqlite')
            cursor.close()
            connection.close()
            
    except:
        logging.exception('unknown error')
