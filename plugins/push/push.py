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
from email.utils import formatdate # need for confirm to RFC2822 standard
from email.utils import make_msgid # need for confirm to RFC2822 standard        
from email.header import Header
from email.mime.text import MIMEText
from includes.helper import alarmHelper


def onLoad():
    try:
        pass
    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
        raise


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
            alarm = alarmHelper.convertAlarm(data['msg'])
            
            if not alarmHelper.checkBlacklist(alarm):
                subject = 'Alarm: ' + data['ric'] + data['functionChar']
            
                mailtext = ''
                mailtext += 'Datum: ' + time.strftime('%d.%m.%Y') + ' ' + time.strftime('%H:%M:%S') + '\n'
                mailtext += 'Einsatz-Nr: ' + alarm['alarmnumber'] + '\n'
                mailtext += 'Kategorie: ' + alarm['category'] + '\n'
                mailtext += 'Stichwort: ' + alarm['keyword'] + '\n'
                mailtext += 'Nachricht: ' + alarm['message'] + '\n'
                mailtext += 'Strasse: ' + alarm['street'] + ' ' + alarm['street_addition'] + '\n'
                mailtext += 'Ort: ' + alarm['country'] + '\n'
                mailtext += 'Anrufer : ' + alarm['caller'] + '\n'
                
                #cat = data['msg'].split('/')[0][-1:].strip() 
                # if cat == 'B' or cat == 'H' or cat == 'S' or cat == 'P' or cat == 'T': 
            
                try:
                    msg = MIMEText(mailtext, 'plain', 'utf-8')
                    msg['From'] = globals.sender
                    msg['Bcc'] = globals.reciever
                    msg['Subject'] = Header(subject, 'utf-8')
                    msg['Date'] = formatdate()
                    msg['Message-Id'] = make_msgid()
                    
                    if any(alarm['category'] in s for s in {'B', 'H', 'S', 'P', 'T'}):
                        logging.debug('sending email with URGENT priority')
                        msg['Priority'] = 'urgent'
                    else:
                        logging.debug('sending email with NORMAL priority')
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