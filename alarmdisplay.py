#!/usr/bin/python
# -*- coding: cp1252 -*-

import os
import logging
import logging.handlers

from includes import globals
import subprocess
from sys import stderr

# This Class extended the TimedRotatingFileHandler with the possibility to change the backupCount after initialization.
class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    #Extended Version of TimedRotatingFileHandler
    def setBackupCount(self, backupCount):
        #Set/Change backupCount
        self.backupCount = backupCount

try:
    try:
        globals.script_path = os.path.dirname(os.path.abspath(__file__))
        globals.database = globals.script_path + '\sql\alarmdisplay.db'
        
        if not os.path.exists(globals.script_path+'/log/'):
                os.mkdir(globals.script_path+'/log/')
                
        myLogger = logging.getLogger()
        myLogger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(module)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
        
        fh = MyTimedRotatingFileHandler(globals.script_path+"/log/boswatch.log", "midnight", interval=1, backupCount=999)
        fh.setLevel(logging.DEBUG) 
        fh.setFormatter(formatter)
        myLogger.addHandler(fh)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        myLogger.addHandler(ch)
    except:
        logging.exception('cannot create logger')
    else:
        
        try:
            #fh.rollover()
            rtl_log = open(globals.script_path+'/log/rtl_fm.log', 'w')
            mon_log = open(globals.script_path+'/log/multimon.log', 'w')
            rtl_log.write('')
            mon_log.write('')
            rtl_log.close()
            mon_log.close()
            logging.debug('Alarmdisplay has started')
            logging.debug('Logfiles cleared')
            ch.setLevel(logging.DEBUG)
        except:
            logging.exception('cannot clear logfiles')
        else:
            
            try:
                logging.debug('set loglevel of fileHandler to: %s',10)
                fh.setLevel(10)
                logging.debug('set backupCount of fileHandler to: %s', 7)
                fh.setBackupCount(7)
            except:
                logging.exception('cannot set loglevel of fileHandler')
             
            from includes import pluginLoader
            pluginLoader.loadPlugins() 
             
            try:
                logging.debug('starting both')
                rtl_fm = subprocess.Popen('rtl_fm -f 169.890M -s 22050 | multimon-ng -t raw -a POCSAG1200 -f alpha -t raw /dev/stdin',
                               # stdin=rtl_fm.stdout,
                               stdout=subprocess.PIPE,
                               stderr=open(globals.script_path + '/log/rtl_fm.log', 'a'),
                               shell=True)
            except:
                logging.exception('cannot start rtl_fm')
                
            #===================================================================
            # try:
            #     logging.debug('starting rtl_fm')
            #     rtl_fm = subprocess.Popen('rtl_fm -f 169.890M -s 22050',
            #                    # stdin=rtl_fm.stdout,
            #                    stdout=subprocess.PIPE,
            #                    stderr=open(globals.script_path + '/log/rtl_fm.log', 'a'),
            #                    shell=True)
            # except:
            #     logging.exception('cannot start rtl_fm')
            # else:
            #     
            #     try:
            #         logging.debug('starting multimon-ng')
            #         multimon_ng = subprocess.Popen('multimon-ng -t raw -a POCSAG1200 -f alpha -t raw /dev/stdin - ',
            #                                        stdin=rtl_fm.stdout,
            #                                        stdout=subprocess.PIPE,
            #                                        stderr=open(globals.script_path+"/log/multimon.log","a"),
            #                                        shell=True)
            #     except:
            #         logging.exception('cannot start multimon-ng')
            #===================================================================
            else:
                    
                    logging.debug('start decoding')
                    
                    while True:
                        decoded = str(rtl_fm.stdout.readline())
                        
                        from includes import decoder
                        decoder.decode(123,decoded)
                        
except KeyboardInterrupt:
    logging.warning('Keyboard Interrupt')
except:
    logging.exception("unknown error")
finally:
    try:
        logging.debug('Alarmdisplay shutting down')
        rtl_fm.terminate()
        logging.debug('rtl_fm terminated')
        #multimon_ng.terminate()
        logging.debug('multimon_ng terminated')
        logging.debug('exiting Alarmdisplay')
    except:
        logging.warning('failed in clean-up routine')
    finally:
        logging.debug('closing logging')
        logging.info('Alarmdisplay exit()')
        logging.shutdown()
        fh.close()
        ch.close()
        exit(0)
                        
