#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

def decode(freq,decoded):
    try:
        if "POCSAG1200" in decoded:
            logging.debug("recieved POCSAG")
            from includes.decoders import poc
            poc.decode(freq,decoded)
    except:
        logging.exception('cannot start decoder')