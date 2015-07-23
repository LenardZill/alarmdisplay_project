#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Email Plugin send an alarm via Email.

@author: Lenard Zill
'''

import logging
import smtplib

from includes import globals
import time
from email.mime.text import MIMEText
from email.utils import formatdate # need for confirm to RFC2822 standard
from email.utils import make_msgid # need for confirm to RFC2822 standard

def run(typ,freq,data):
    try:
        server = smtplib.SMTP(globals.smtp_server)
        server.starttls()
        server.login(globals.user, globals.password)
    except:
        logging.error('cannot connect to email')
        logging.debug('cannot connect to email', exc_info=True)
        return
    else:
        try:
            logging.debug('Start POC to email')
            subject = globals.subject
            subject = subject.replace('%RIC%', data['ric'])
            subject = subject.replace('%FUNC%', data['function']).replace('%FUNCCHAR%', data['functionChar'])
            subject = subject.replace('%MSG%', data['msg'])
            subject = subject.replace('%DESCR%', data['description'])
            subject = subject.replace('%TIME%', time.strftime('H:M:S').replace('%DATE%', time.strftime('Y-m-d')))
        
            mailtext = globals.message
            mailtext = mailtext.replace('%RIC%', data['ric'])
            mailtext = mailtext.replace('%FUNC%', data['function']).replace('%FUNCCHAR%', data['functionChar'])
            mailtext = mailtext.replace('%MSG%', data['msg'])
            mailtext = mailtext.replace('%DESCR%', data['description'])
            mailtext = mailtext.replace('%TIME%', time.strftime('%H:%M:%S').replace('%DATE%', time.strftime('%Y-%m-%d')))
            
            
            try:
                msg = MIMEText(mailtext)
                msg['From'] = globals.sender
                msg['To'] = globals.reciever
                msg['Subject'] = subject
                msg['Date'] = formatdate()
                msg['Message-Id'] = make_msgid()
                msg['Priority'] = 'normal'
                server.sendmail(globals.sender, globals.reciever.split(), msg.as_string())
            except:
                logging.error('send email failed')
                logging.debug('send email failed', exc_info=True)
                raise
        except:
            logging.error('poc to email failed')
            logging.debug('poc to email failed', exc_info=True)
            return
        
    finally:
        logging.debug("close email connection")
        try:
            server.quit()
        except:
            pass