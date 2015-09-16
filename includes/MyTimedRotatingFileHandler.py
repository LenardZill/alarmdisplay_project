#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Created on 16.09.2015

@author: LZill
'''

import logging

class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """Extended Version of TimedRotatingFileHandler"""
    def setBackupCount(self, backupCount):
        """Set/Change backupCount"""
        self.backupCount = backupCount