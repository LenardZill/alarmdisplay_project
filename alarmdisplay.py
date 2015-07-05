#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import logging.handlers

import os
import argparse 
import time
import subprocess

from includes import globals
from includes import checkSubprocesses

# This Class extended the TimedRotatingFileHandler with the possibility to change the backupCount after initialization.
class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    #Extended Version of TimedRotatingFileHandler
    def setBackupCount(self, backupCount):
        #Set/Change backupCount
        self.backupCount = backupCount

#
# ArgParser
# Have to be before main program
#
try:
    # With -h or --help you get the Args help
    parser = argparse.ArgumentParser(prog="alarmdisplay.py",
                                     description="no description")
    parser.add_argument("-f", "--freq", help="Frequency you want to listen", required=True)
    parser.add_argument("-d", "--device", help="Device you want to use (Check with rtl_test)", type=int, default=0)
    parser.add_argument("-s", "--squelch", help="Level of squelch", type=int, default=0)
    parser.add_argument("-v", "--verbose", help="Shows more information", action="store_true")
    parser.add_argument("-q", "--quiet", help="Shows no information. Only logfiles", action="store_true")
    # We need this argument for testing (skip instantiate of rtl-fm and multimon-ng):
    parser.add_argument("-t", "--test", help=argparse.SUPPRESS, action="store_true")
    args = parser.parse_args()
except SystemExit:
    # -h or --help called, exit right now
    exit(0)
except:
    # we couldn't work without arguments -> exit
    print "ERROR: cannot parsing the arguments"
    exit(1)


# main program
try:
    # initialization
    rtl_fm = None
    multimon_ng = None
    
    try:
        # script-path
        globals.script_path = os.path.dirname(os.path.abspath(__file__))
        
        # database
        globals.database_path = globals.script_path + '\sql\alarmdisplay.db'
        globals.database_table = 'alarmitems'
        
        # log-path
        globals.log_path = globals.script_path + '/log/'
        
        # create log-path if not exists
        if not os.path.exists(globals.log_path):
            os.mkdir(globals.log_path)
    except:
        # couldn't work without logging
        print 'ERROR: cannot initialize paths'
        exit(1)
    
    # create new myLogger
    try:                
        myLogger = logging.getLogger()
        myLogger.setLevel(logging.DEBUG)
        # set log strign format
        formatter = logging.Formatter('%(asctime)s - %(module)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')
        # create a file logger
        fh = MyTimedRotatingFileHandler(globals.log_path+'alarmdisplay.log', 'midnight', interval=1, backupCount=999)
        # starts with log level debug
        fh.setLevel(logging.DEBUG) 
        fh.setFormatter(formatter)
        myLogger.addHandler(fh)
        # create a display logger
        ch = logging.StreamHandler()
        # loglevel for display
        if args.verbose:
            ch.setLevel(logging.DEBUG)
        elif args.quiet:
            ch.setLevel(logging.CRITICAL)
        else:
            ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        myLogger.addHandler(ch)
    except:
        # we couldn't work without logging
        print "ERROR: cannot create logger"
        exit(1)
    
    # clear the logfiles
    try:
        fh.doRollover()
        rtl_log = open(globals.log_path + 'rtl_fm.log', 'w')
        mon_log = open(globals.log_path+"multimon.log", "w")
        rtl_log.write('')
        mon_log.write('')
        rtl_log.close()
        mon_log.close()
        logging.debug('Alarmdisplay has started')
        logging.debug('Logfiles cleared')
    except:
        # it's an error, but we could work without it
        logging.error('cannot clear logfiles')
        logging.debug("cannot clear Logfiles", exc_info=True)
        pass
    
    # for debug args
    try:
        logging.debug('Alarmdisplay givven arguments')
        
        if args.test:
            logging.debug(' - Test-Mode!')
            
        logging.debug(' - Frequency: %s', args.freq)
        logging.debug(' - Device: %s', args.device)
        logging.debug(' - Squelch: %', args.squelch)
        
        demodulation = '-a POCSAG1200'
        logging.debug(' - Demod: POC1200')
        
        logging.debug(' - Verbose Mode: %s', args.verbose)
        logging.debug(' - Quiet Mode: %s', args.quiet)
        
        if args.test:
            logging.warning("!!! We are in Test-Mode !!!")
    except:
        # we couldn't work without config
        logging.critical('cannot display/log args')
        logging.debug('cannto display/log args', exc_info=True)
        exit(1)
    
    # set the loglevel and backupCount of the file handler
    try:
        logging.debug('set loglevel of fileHandler to: %s',10)
        fh.setLevel(10)
        logging.debug('set backupCount of fileHandler to: %s', 7)
        fh.setBackupCount(7)
    except:
        # it's an error, but we could work without it
        logging.error('cannot set loglevel of fileHandler')
        logging.debug('cannto set loglevel of fileHandler', exc_info=True)
        pass
        
    # load plugins     
    try:
        from includes import pluginLoader
        pluginLoader.loadPlugins()
    except:
        # we couldn't work without plugins
        logging.critical("cannot load plugins")
        logging.debug("cannot load plugins", exc_info=True)
        exit(1) 
    
    # start rtl_fm         
    try:
        if not args.test:
            logging.debug('starting rtl_fm')
            rtl_fm = subprocess.Popen('rtl_fm -f 169.890M -s 22050 | multimon-ng -t raw -a POCSAG1200 -f alpha -t raw /dev/stdin',
                            stdout=subprocess.PIPE,
                            stderr=open(globals.log_path + 'rtl_fm.log', 'a'),
                            shell=False)
            time.sleep(3)
            checkSubprocesses.checkRTL()
        else:
            logging.warning('! Test-Mode: rtl_fm not started !')
    except:
        # we couldn't work without rtl_fm
        logging.critical('cannot start rtl_fm')
        logging.debug('cannot start rtl_fm', exc_info=True)
        exit(1)
        
    # start multimon         
    try:
        if not args.test:
            logging.debug('starting multimon-ng')
            rtl_fm = subprocess.Popen('rtl_fm -f 169.890M -s 22050 | multimon-ng -t raw -a POCSAG1200 -f alpha -t raw /dev/stdin',
                            stdin=rtl_fm.stdout,
                            stdout=subprocess.PIPE,
                            stderr=open(globals.log_path + 'multimon.log', 'a'),
                            shell=False)
            time.sleep(3)
            checkSubprocesses.checkMultimon()
        else:
            logging.warning('! Test-Mode: multimon-ng not started !')
    except:
        # we couldn't work without multimon-ng
        logging.critical('cannot start multimon-ng')
        logging.debug('cannot start multimon-ng', exc_info=True)
        exit(1)

    logging.debug('start decoding')
                    
    while True:
        if not args.test:
            # get line data from multimon stdout
            decoded = str(rtl_fm.stdout.readline())
        else:
            decoded = "POCSAG1200: Address: 1234567 Function: 1 Alpha: Hello World"
            time.sleep(1)
                        
        from includes import decoder
        decoder.decode(args.freq,decoded)
                        
except KeyboardInterrupt:
    logging.warning('Keyboard Interrupt')
except SystemExit:
    logging.warning('SystemExit recieved')
    exit()
except:
    logging.exception('unknown error')
finally:
    try:
        logging.debug('Alarmdisplay shutting down')
        if multimon_ng and multimon_ng.pid:
            logging.debug('terminate multimon-ng (%s)', multimon_ng.pid)
            multimon_ng.terminate()
            multimon_ng.wait()
            logging.debug('multimon-ng terminated')
        if rtl_fm and rtl_fm.pid:
            logging.debug('terminate rtl_fm (%s)', rtl_fm.pid)
            rtl_fm.terminate()
            rtl_fm.wait()
            logging.debug('rtl_fm terminated')
        logging.debug('exiting Alarmdisplay')
    except:
        logging.warning("failed in clean-up routine")
        logging.debug("failed in clean-up routine", exc_info=True)
    
    finally:
        # close logging
        logging.debug('closing logging')
        logging.info('Alarmdisplay exit()')
        logging.shutdown()
        fh.close()
        ch.close()