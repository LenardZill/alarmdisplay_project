#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import MySQLdb

from includes import globals
from includes.helper import alarmHelper


def onload():
    try:
        pass
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
        raise


def isallowed(category):
    if globals.config.get('POC', 'blacklist_categories'):
        if category not in globals.config.get('POC', 'blacklist_categories'):
            logging.info('Category %s is allowed', category)
            return True
        else:
            logging.info('Category %s is not allowed', category)
            return False
    return True


def run(typ, freq, data):
    try:
        try:
            logging.debug('connect to MySQL')
            connection = MySQLdb.connect(host=globals.config.get('MySQL', 'dbserver'),
                                         user=globals.config.get('MySQL', 'dbuser'),
                                         passwd=globals.config.get('MySQL', 'dbpassword'),
                                         db=globals.config.get('MySQL', 'database'))
            cursor = connection.cursor()
        except:
            logging.error('cannot connect to MySQL')
            logging.debug('cannot connect to MySQL', exc_info=True)
            return
        else:
            try:
                alarm = alarmHelper.convertalarm(data['msg'])
                if isallowed(alarm['category']):
                    logging.debug('Insert POC')
                    cursor.execute('INSERT INTO '+globals.config.get('MySQL', 'table') +
                                    ' (time,ric,funktion,funktionChar,msg,bitrate,description,'
                                    'alarmnumber,category,keyword,street,street_addition,country,caller,message) '
                                    'VALUES (NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                    (data['ric'], data['function'], data['functionChar'], data['msg'],
                                    data['bitrate'], data['description'],
                                    alarm['alarmnumber'], alarm['category'], alarm['keyword'], alarm['street'],
                                    alarm['street_addition'], alarm['country'], alarm['caller'], alarm['message']))
            except:
                logging.error('cannot Insert POC')
                logging.debug('cannot Insert POC')
                return
            finally:
                logging.debug('close mysql')
                try:
                    cursor.close()
                    connection.close()
                except:
                    pass
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
