#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

def decode(freq,decoded):
    try:
        if "POCSAG" in decoded:
            from includes.decoders import poc
            logging.debug('POCSAG RECIEVED')
            poc.decode(freq,decoded)
    except:
        logging.exception('cannot start decoder')