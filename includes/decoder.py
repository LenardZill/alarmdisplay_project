#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging

def decode(freq,decoded):
    try:
        from includes.decoders import poc
        poc.decode(freq,decoded)
    except:
        logging.exception('cannot start decoder')