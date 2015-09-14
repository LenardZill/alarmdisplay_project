#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Created on 14.09.2015

@author: LZill
'''

import logging
from includes import globals

def convertAlarm(alarmLine):
    try:
            logging.debug('start to convertAlarm')
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
            
            #remove duplicated spaces
            alarmnumber = ' '.join(alarmnumber.split())
            category = ' '.join(category.split())
            keyword = ' '.join(keyword.split())
            street = ' '.join(street.split())
            street_addition = ' '.join(street_addition.split())
            country = ' '.join(country.split())
            caller = ' '.join(caller.split())
            message = ' ' .message.join(message.split())
            
            alarm = {'alarmnumber': alarmnumber, 'category': category, 'keyword': keyword, 'street': street, 'street_addition': street_addition, 'country': country, 'caller': caller, 'message': message}
            return alarm
    except:
        logging.warning('error in convertAlarm')
        logging.debug('error in convertAlarm', exc_info=True)
        return None
    
def checkWhitelist(alarm):
    try:
        if not globals.whitelist:
            logging.debug('there is no Whitelist')
            return True
        
        if any(alarm['category']in s for s in globals.whitelist):
            logging.debug('Alarm is on Whitelist')
            return True
        else:
            logging.debug('Alarm is not on Whitelist')
            return False
    except:
        logging.warning('error in checkWhitelist')
        logging.debug('error in checkWhitelist', exc_info=True)
        return False