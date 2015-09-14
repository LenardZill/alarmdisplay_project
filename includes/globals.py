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

# sqlite
database_path = ''
database_path = 'alarmitems'

# email
smtp_server = ''
smtp_port = ''

user = ''
password = ''

sender = ''
reciever = ''

subject = 'Alarm: %RIC%%FUNCCHAR%'
message = '%DATE% %TIME%: %MSG%'

# double alarm
poc_id_old = 0
poc_time_old = 0

# pluginLoader
pluginList = {}