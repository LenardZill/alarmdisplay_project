#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Created on 16.09.2015

@author: LZill
'''

import logging

import MySQLdb

from includes import globals
from includes.helper import alarmHelper

def onLoad():
    try:
        pass
    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
        raise


def run(typ,freq,data):
    try:
        try:
            logging.debug("connect to MySQL")
            connection = MySQLdb.connect(host = globals.config.get("MySQL","dbserver"), user = globals.config.get("MySQL","dbuser"), passwd = globals.config.get("MySQL","dbpassword"), db = globals.config.get("MySQL","database"))
            cursor = connection.cursor()
        except:
            logging.error("cannot connect to MySQL")
            logging.debug("cannot connect to MySQL", exc_info=True)
        else:
            try:
                if alarmHelper.isValid(data['msg']):
                    logging.debug('Insert POC')
                    cursor.execute("INSERT INTO "+globals.config.get("MySQL","table")+" (time,ric,funktion,funktionChar,msg,bitrate,description) VALUES (NOW(),%s,%s,%s,%s,%s,%s)",(data["ric"],data["function"],data["functionChar"],data["msg"],data["bitrate"],data["description"]))
            except:
                logging.error('cannot Insert POC')
                logging.debug('cannot Insert POC')
                return
            finally:
                logging.debug("close mysql")
                try:
                    cursor.close()
                    connection.close()
                except:
                    pass
    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)