#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

from includes import globals


def checkrtl():
    try:
        rtllog = open(globals.log_path+'rtl_fm.log', 'r').read()
        if ('exiting' in rtllog) or ('Failed to open' in rtllog):
            logging.debug('\n%s', rtllog)
            raise OSError('starting rtl_fm returns an error')
    except OSError:
        raise
    except:
        logging.critical('cannot check rtl_fm.log')
        logging.debug('cannot check rtl_fm.log', exc_info=True)
        raise


def checkmultimon():
    try:
        multimonlog = open(globals.log_path+'multimon.log', 'r').read()
        if ('invalid' in multimonlog) or ('error' in multimonlog):
            logging.debug('\n%s', multimonlog)
            raise OSError('starting multimon-ng returns an error')
    except OSError:
        raise
    except:
        logging.critical('cannot check multimon.log')
        logging.debug('cannot check multimon.log', exc_info=True)
        raise
