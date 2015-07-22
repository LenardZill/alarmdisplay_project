#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

def decode(freq,decoded):
    try:
        if "POCSAG" in decoded:
            logging.debug('recieved pocsag (' + decoded + ')')
            from includes.decoders import poc
            poc.decode(freq,decoded)
    except:
        logging.exception('cannot start decoder')