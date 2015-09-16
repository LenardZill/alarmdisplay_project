#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Created on 14.09.2015

@author: LZill
'''

import logging
from includes import globals

def isValid(alarmLine):
    if convertAlarm(alarmLine) is None:
        return False
    else:
        return True

def convertAlarm(alarmLine):
    try:
            logging.debug('start to convertAlarm')
            try:
                
                split = alarmLine.split('/')
                alarmnumber = split[0][-6:-1].strip()
                category = split[0][-1:].strip()
                keyword = split[1].split(')')[0].strip()
                street = split[3].replace('(', ' ').replace(')', '').strip()
                street_addition = split[2].split(':')[1].split('(')[0].strip()
                country = split[2].split(':')[0].strip()
                caller = split[2].split('(')[-1].replace(')', '').strip()
                
                message = ''
                messagelist = split[4:]
                for entry in messagelist:
                    message += entry.strip() + ' '
                    message = message.strip()
            except:
                logging.info('failed to convert alarm')
                return None
            
            alarmnumber = ' '.join(alarmnumber.split())
            category = ' '.join(category.split())
            keyword = ' '.join(keyword.split())
            street = ' '.join(street.split())
            street_addition = ' '.join(street_addition.split())
            country = ' '.join(country.split())
            caller = ' '.join(caller.split())
            message = ' ' .join(message.split())
            
            alarm = {'alarmnumber': alarmnumber, 'category': category, 'keyword': keyword, 'street': street, 'street_addition': street_addition, 'country': country, 'caller': caller, 'message': message}
            return alarm
    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
        return None