#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
POCSAG Decoder

@author: Lenard Zill
'''

import time
import logging 
import re 

from includes import globals

def decode(freq,decoded):
    bitrate = 0
    timestamp = int(time.time())
    
    if not 'Enabled demodulators:' in decoded:
        if 'POCSAG1200' in decoded:
            bitrate = 12000
            poc_id = decoded[21:28].replace(' ', '').zfill(7)
            poc_sub = decoded[40].replace('3', '4').replace('2', '3').replace('1', '2').replace('0', '1')
        
        if bitrate == 0:
            logging.warning('POCSAG Bitrate not found')
            logging.debug(' - (%s)', decoded)
        else:
            logging.debug('POCSAG Bitrate: %s', bitrate)
        
            if 'Alpha:    ' in decoded:
                poc_text = decoded.split('Alpha:    ')[1].strip()
            else:
                poc_text = ''
            
            logging.debug('message: ' + poc_text + ' [' + len(poc_text) + ']')
            
            if re.search('[0-9]{7}', poc_id):
                if poc_id == globals.poc_id_old and timestamp < globals.poc_time_old + 5:
                    logging.info('POCSAG%s double alarm: %s within %s second(s)', bitrate, globals.poc_id_old, timestamp-globals.poc_time_old)
                    globals.poc_time_old = timestamp
                else:
                    logging.info('POCSAG%s: %s %s %s ', bitrate, poc_id, poc_sub, poc_text)
                    data = {'ric':poc_id, 'function':poc_sub, 'msg': poc_text, 'bitrate':bitrate, 'description':poc_id}
                    data['functionChar'] = data['function'].replace('1', 'a').replace('2', 'b').replace('3', 'c').replace('4', 'd')
                
                    from includes import alarmHandler
                    alarmHandler.processAlarm("POC",freq,data)
                    globals.poc_id_old = poc_id
                    globals.poc_time_old = timestamp
            else:
                logging.warning('No valid POCSAG%s RIC: %s', bitrate, poc_id)
