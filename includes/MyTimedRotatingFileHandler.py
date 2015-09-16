#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging


class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def setbackupcount(self, backupcount):
        self.backupcount = backupcount
