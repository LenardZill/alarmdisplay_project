#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
            data['msg'] = data['msg']
            
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
            mailtext = mailtext.replace('%TIME%', time.strftime('%H:%M:%S')).replace('%DATE%', time.strftime('%Y-%m-%d'))
            
            split = data['msg'].split('/')
            alarmnumber = split[0][-6:-1].strip()
            category = split[0][-1:].strip()
            keyword = split[1].split(')')[0].strip()
            street = split[3].replace('(', ' ').replace(')', '').strip()
            street_addition = split[2].split(':')[1].split('(')[0].strip()
            country = split[2].split(':')[0].strip()
            caller = split[2].split('(')[-1].replace(')', '').strip()
            
            message = ''
            messagelist = split[4:]
            for entry in messagelist:
                message += entry.strip() + ' '
            message = message.strip()
            
            mailtext = ''
            mailtext += 'Datum: ' + time.strftime('%d.%m.%Y') + ' ' + time.strftime('%H:%M:%S') + '\n'
            mailtext += 'Einsatz-Nr: ' + alarmnumber + '\n'
            mailtext += 'Kategorie: ' + category + '\n'
            mailtext += 'Stichwort: ' + keyword + '\n'
            mailtext += 'Nachricht: ' + message + '\n'
            mailtext += 'Strasse: ' + street + ' ' + street_addition + '\n'
            mailtext += 'Ort: ' + country + '\n'
            mailtext += 'Anrufer : ' + caller + '\n'
            
            #cat = data['msg'].split('/')[0][-1:].strip() 
            # if cat == 'B' or cat == 'H' or cat == 'S' or cat == 'P' or cat == 'T': 
            
            try:
                msg = MIMEText(mailtext)
                msg['From'] = globals.sender
                msg['To'] = globals.reciever
                msg['Subject'] = subject
                msg['Date'] = formatdate()
                msg['Message-Id'] = make_msgid()
                if category == 'B' or category == 'H' or category == 'S' or category == 'P' or category == 'T':
                    msg.add_header('X-Priority','1')
                else:
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