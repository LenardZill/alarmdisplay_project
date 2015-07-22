#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Email Plugin send an alarm via Email.

@author: Lenard Zill
'''

import logging
import smtplib

from includes import globals
from smtplib import SMTPException

def run(typ,freq,data):
    try:
        message = """From: Alarmdisplay <raspberry@lenardzill.de>
To: To Person <raspberry@lenardzill.de>
Subject: Alarmdisplay e-mail test

This is a test e-mail message.
"""

        smtpObj = smtplib.SMTP('smtp.strato.de')
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(globals.username, globals.password)
        smtpObj.sendmail(globals.sender, globals.reciever, message)
        smtpObj.quit()
    except SMTPException:
        logging.exception('unable to send email')
    except:
        logging.exception('unknown error')
