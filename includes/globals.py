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
table = 'alarmitems'

# email
smtp_server = ''
user = 'aspberry@lenardzill.de'
password = 'Len!9409'

sender = 'raspberry@lenardzill.de'
reciever = 'raspberry@lenardzill.de'

subject = 'Alarm: %RIC%%FUNCCHAR%'
message = '%DATE% %TIME%: %MSG%'

# double alarm
poc_id_old = 0
poc_time_old = 0

# pluginLoader
pluginList = {}