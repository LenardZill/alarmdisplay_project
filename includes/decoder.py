#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging

def decode(freq,decoded):
    try:
        if "POCSAG" in decoded:
            
            from includes.decoders import poc
            poc.decode(freq,decoded)
    except:
        logging.exception('cannot start decoder')