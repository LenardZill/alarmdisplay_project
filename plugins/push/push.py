#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import smtplib

import time
from email.utils import formatdate
from email.utils import make_msgid
from email.mime.text import MIMEText
from includes.helper import alarmHelper

from includes import globals


def onload():
    try:
        pass
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
        raise


def isallowed(category):
    if globals.config.get('POC', 'blacklist_categories'):
        if category not in globals.config.get('POC', 'blacklist_categories'):
            logging.info('Category %s is allowed', category)
            return True
        else:
            logging.info('Category %s is not allowed', category)
            return False
    return True

def run(typ, freq, data):
    try:
        try:
            server = smtplib.SMTP(globals.config.get('push', 'smtp_server'), globals.config.get('push', 'smtp_port'))
            server.set_debuglevel(0)
            if globals.config.get('push', 'tls'):
                        server.starttls()
            if globals.config.get('push', 'user'):
                        server.login(globals.config.get('push', 'user'), globals.config.get('push', 'password'))
        except:
            logging.error('cannot connect to push')
            logging.debug('cannot connect to push', exc_info=True)
            return
        else:
            try:
                if alarmHelper.isvalid(data['msg']):
                    alarm = alarmHelper.convertalarm(data['msg'])
                    if isallowed(alarm['category']):
                        logging.debug('Start POC to push')
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
                        try:
                            msg = MIMEText(mailtext, 'plain', 'utf-8')
                            msg['From'] = globals.config.get('push', 'from')
                            msg['To'] = globals.config.get('push', 'to')
                            msg['Subject'] = subject
                            msg['Date'] = formatdate()
                            msg['Message-Id'] = make_msgid()
                            msg['Priority'] = globals.config.get('push', 'priority')
                            server.sendmail(globals.config.get('push', 'from'),
                                            globals.config.get('push', 'to').split(),
                                            msg.as_string())
                        except:
                            logging.error('send push failed')
                            logging.debug('send push failed', exc_info=True)
                            raise
            except:
                logging.error('POC to push failed')
                logging.debug('POC to push failed', exc_info=True)
                return
        finally:
            logging.debug('close push-connection')
            try:
                server.quit()
            except:
                pass
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
