#!/usr/bin/python
# -*- coding: cp1252 -*-

"""
Global variables

@author: Lenard Zill
"""

# Global variables
config = 0
script_path = ''
log_path = ''


# double alarm
doubleList = []

# sqlite
database_path = ''
database_table = 'alarmitems'

# email
smtp_server = ''
smtp_port = ''

user = ''
password = ''

sender = ''
reciever = ''

# pluginLoader
pluginList = {}

#alarmHelper
blacklist = {}

def getVers(mode="vers"):
    if mode == "vers":
        return "1.0"
    elif mode == "date":
        return " 2015/09/16"