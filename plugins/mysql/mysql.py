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


def isAllowed(category):
    if globals.config.get('POC', 'blacklist_categories'):
        if not category in globals.config.get('POC', 'blacklist_categories'):
            logging.info('Category %s is allowed', category)
            return True
        else:
            logging.info('Category %s is not allowed', category)
            return False
    return True


def run(typ,freq,data):
    try:
        try:
            logging.debug("connect to MySQL")
            connection = MySQLdb.connect(host = globals.config.get("MySQL","dbserver"), user = globals.config.get("MySQL","dbuser"), passwd = globals.config.get("MySQL","dbpassword"), db = globals.config.get("MySQL","database"))
            cursor = connection.cursor()
        except:
            logging.error("cannot connect to MySQL")
            logging.debug("cannot connect to MySQL", exc_info=True)
            return
        else:
            try:
                if alarmHelper.isValid(data['msg']):
                    alarm = alarmHelper.convertAlarm(data['msg'])
                    if isAllowed(alarm['category']):
                        logging.debug('Insert POC')
                        cursor.execute("INSERT INTO "+globals.config.get("MySQL","table")+" (time,ric,funktion,funktionChar,msg,bitrate,description) VALUES (NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                       (data["ric"],data["function"],data["functionChar"],data["msg"],data["bitrate"],data["description"],
                                        alarm['alarmnumber'],alarm['category'],alarm['keyword'],alarm['street'],alarm['street_addition'],alarm['country'],alarm['caller'],alarm['message']))
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