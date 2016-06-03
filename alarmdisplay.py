#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import logging.handlers
import argparse
import ConfigParser
import os
import time
import subprocess

from includes import globals
from includes import MyTimedRotatingFileHandler
from includes import checkSubprocesses

try:
    parser = argparse.ArgumentParser(prog='alarmdisplay.py',
                                     description='no description',
                                     epilog='More options yous can find in the extern config.ini file')
    parser.add_argument("-f", "--freq", help="Frequency you want to listen", required=True)
    parser.add_argument("-v", "--verbose", help="Shows more information", action="store_true")
    parser.add_argument("-q", "--quiet", help="Shows no information. Only logfiles", action="store_true")
    parser.add_argument("-t", "--test", help=argparse.SUPPRESS, action="store_true")
    args = parser.parse_args()
except SystemExit:
    exit(0)
except:
    print "ERROR: cannot parsing the arguments"
    exit(1)


try:
    rtl_fm = None
    multimon_ng = None

    try:
        globals.script_path = os.path.dirname(os.path.abspath(__file__))
        globals.log_path = globals.script_path + '/log/'
        
        if not os.path.exists(globals.log_path):
            os.mkdir(globals.log_path)
    except:
        print 'ERROR: cannot initialize paths'
        exit(1)

    try:
        myLogger = logging.getLogger()
        myLogger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(module)-15s [%(levelname)-8s] %(message)s', '%d.%m.%Y %H:%M:%S')

        fh = MyTimedRotatingFileHandler.MyTimedRotatingFileHandler(globals.log_path+'alarmdisplay.log', 'midnight',
                                                                   interval=1, backupCount=999)

        fh.setLevel(logging.DEBUG) 
        fh.setFormatter(formatter)
        myLogger.addHandler(fh)

        ch = logging.StreamHandler()

        if args.verbose:
            ch.setLevel(logging.DEBUG)
        elif args.quiet:
            ch.setLevel(logging.CRITICAL)
        else:
            ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        myLogger.addHandler(ch)
    except:
        print "ERROR: cannot create logger"
        exit(1)

    try:
        fh.doRollover()
        rtl_log = open(globals.log_path + 'rtl_fm.log', 'w')
        mon_log = open(globals.log_path + 'multimon.log', 'w')
        rtl_log.write('')
        mon_log.write('')
        rtl_log.close()
        mon_log.close()
        logging.debug('Alarmdisplay has started')
        logging.debug('Logfiles cleared')
    except:
        logging.error('cannot clear logfiles')
        logging.debug("cannot clear Logfiles", exc_info=True)
        pass

    try:
        logging.debug('SW Version:    %s', globals.getvers('vers'))
        logging.debug('Build Date:    %s', globals.getvers('date'))
        logging.debug('Alarmdisplay givven arguments')
        
        if args.test:
            logging.debug(' - Test-Mode!')
            
        logging.debug(' - Frequency: %s', args.freq)
        
        logging.debug(' - Demod: POC1200')
        
        logging.debug(' - Verbose Mode: %s', args.verbose)
        logging.debug(' - Quiet Mode: %s', args.quiet)
        
        if args.test:
            logging.warning("!!! We are in Test-Mode !!!")
    except:
        logging.critical('cannot display/log args')
        logging.debug('cannot display/log args', exc_info=True)
        exit(1)

    try:
        logging.debug('reading config file')
        globals.config = ConfigParser.ConfigParser()
        globals.config.read(globals.script_path + '/config/config.ini')
        
        if globals.config.getint('Alarmdisplay', 'loglevel') == 10:
            logging.debug(' - Alarmdisplay:')
            for key, val in globals.config.items('Alarmdisplay'):
                logging.debug(' -- %s = %s', key, val)
            logging.debug(' - POC:')
            for key, val in globals.config.items('POC'):
                logging.debug(' -- %s = %s', key, val)
    except:
        logging.critical('cannot read config file')
        logging.debug('cannot read config file', exc_info=True)
        exit(1)

    try:
        logging.debug('set loglevel of fileHandler to: %s', globals.config.getint("Alarmdisplay", "loglevel"))
        fh.setLevel(globals.config.getint("Alarmdisplay", "loglevel"))
        logging.debug("set backupCount of fileHandler to: %s", globals.config.getint("Alarmdisplay", "backupCount"))
        fh.setbackupcount(globals.config.getint("Alarmdisplay", "backupCount"))
    except:
        logging.error('cannot set loglevel of fileHandler')
        logging.debug('cannot set loglevel of fileHandler', exc_info=True)
        pass
   
    try:
        from includes import pluginLoader
        pluginLoader.loadplugins()
    except:
        logging.critical("cannot load plugins")
        logging.debug("cannot load plugins", exc_info=True)
        exit(1) 

    try:
        if globals.config.getboolean("Alarmdisplay", "useRegExFilter"):
            from includes import filter
            filter.loadFilters()
    except:
		logging.error("cannot load filters")
		logging.debug("cannot load filters", exc_info=True)
		pass

    try:
        if globals.config.getboolean('POC', 'idDescribed'):
            from includes import description_list
            description_list.load_description_list()
    except:
        logging.error("cannot load description lists")
        logging.debug("cannot load description lists", exc_info=True)
        pass


    try:
        if not args.test:
            logging.debug('starting rtl_fm')
            command = 'rtl_fm -d 0 -f ' + args.freq + ' -M fm -s 22050 -p 0 -E DC -F 0 -l 0 -g 100'
            rtl_fm = subprocess.Popen(command.split(),
                                      stdout=subprocess.PIPE,
                                      stderr=open(globals.log_path + 'rtl_fm.log', 'a'),
                                      shell=False)
            time.sleep(3)
            checkSubprocesses.checkrtl()
        else:
            logging.warning('! Test-Mode: rtl_fm not started !')
    except:
        logging.critical('cannot start rtl_fm')
        logging.debug('cannot start rtl_fm', exc_info=True)
        exit(1)
    
    try:
        if not args.test:
            logging.debug('starting multimon-ng')
            command = 'multimon-ng -a POCSAG1200 -f alpha -t raw /dev/stdin - '
            multimon_ng = subprocess.Popen(command.split(),
                                           stdin=rtl_fm.stdout,
                                           stdout=subprocess.PIPE,
                                           stderr=open(globals.log_path + 'multimon.log', 'a'),
                                           shell=False)
            time.sleep(3)
            checkSubprocesses.checkmultimon()
        else:
            logging.warning('! Test-Mode: multimon-ng not started !')
    except:
        logging.critical('cannot start multimon-ng')
        logging.debug('cannot start multimon-ng', exc_info=True)
        exit(1)

    if not args.test:
        logging.debug('start decoding')
        while True:
            decoded = multimon_ng.stdout.readline()
            logging.debug(decoded)
            from includes import decoder
            decoder.decode(args.freq, decoded.decode('utf-8'))
    else:
        logging.debug('start testing')
        testFile = open(globals.script_path+"/testdata/testdata.txt", "r")
        for testData in testFile:
            if (len(testData.rstrip(' \t\n\r')) > 1) and ("#" not in testData[0]):
                logging.info("Testdata: %s", testData.rstrip(' \t\n\r'))
                from includes import decoder
                decoder.decode(args.freq, testData)
                time.sleep(1)
        logging.debug("test finished")
                        
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
        logging.debug('closing logging')
        logging.info('Alarmdisplay exit()')
        logging.shutdown()
        fh.close()
        ch.close()
