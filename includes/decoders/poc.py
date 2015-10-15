#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging 
import re 

from includes import globals
from includes import doubleFilter
from includes.helper.alarmHelper import isvalid


def isallowed(poc_id):
    if globals.config.get('POC', 'allow_ric'):
        if poc_id in globals.config.get('POC', 'allow_ric'):
            logging.info('RIC %s is allowed', poc_id)
            return True
        else:
            logging.info('RIC %s is not in the allowed list', poc_id)
            return False
    elif poc_id in globals.config.get('POC', 'deny_ric'):
        logging.info('RIC %s is denied by config.ini', poc_id)
        return False
    elif int(poc_id) < globals.config.getint('POC', 'filter_range_start'):
        logging.info('RIC %s out of filter range (start)', poc_id)
        return False
    elif int(poc_id) > globals.config.getint('POC', 'filter_range_end'):
        logging.info('RIC %s out of filter range (end)', poc_id)
        return False
    return True


def decode(freq, decoded):
    try:
        if 'Enabled demodulators:' not in decoded:
            bitrate = 12000
            poc_id = decoded[21:28].replace(' ', '').zfill(7)
            poc_sub = str(int(decoded[40])+1)
            if 'Alpha:' in decoded:
                poc_text = decoded.split('Alpha:   ')[1].strip()
                if '<NUL>' in poc_text:
                    poc_text = poc_text.split('<NUL>')[0].strip() 
            else:
                poc_text = ''
            if re.search('[0-9]{7}', poc_id) and re.search('[1-4]{1}', poc_sub):
                if isallowed(poc_id):
                    if doubleFilter.checkid('POC', poc_id+poc_sub, poc_text):
                        logging.info('POCSAG%s: %s %s %s ', bitrate, poc_id, poc_sub, poc_text)
                        data = {'ric': poc_id, 'function': poc_sub, 'msg': poc_text,
                                'bitrate': bitrate, 'description': poc_id}
                        data['functionChar'] = data['function'].replace('1', 'a').replace('2', 'b')\
                            .replace('3', 'c').replace('4', 'd')
                        try:
                            if(isvalid(data['msg'])):
                                from includes import alarmHandler
                                alarmHandler.processalarm('POC', freq, data)
                        except:
                            logging.error('processing alarm failed')
                            logging.debug('processing alarm failed', exc_info=True)
                            pass
                    doubleFilter.newentry(poc_id+poc_sub, poc_text)
                else:
                    logging.debug('POCSAG%s: %s is not allowed', bitrate, poc_id)
            else:
                logging.warning('No valid POCSAG%s RIC: %s SUB: %s', bitrate, poc_id, poc_sub)
    except:
        logging.error('error while decoding')
        logging.debug('error while decoding', exc_info=True)    
