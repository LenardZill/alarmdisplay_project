#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging


def isvalid(alarmline):
    if convertalarm(alarmline) is None:
        return False
    else:
        return True


def convertalarm(alarmline):
    try:
        try:
            split = alarmline.split('/')
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
        except:
            return None
        alarmnumber = ' '.join(alarmnumber.split())
        category = ' '.join(category.split())
        keyword = ' '.join(keyword.split())
        street = ' '.join(street.split())
        street_addition = ' '.join(street_addition.split())
        country = ' '.join(country.split())
        caller = ' '.join(caller.split())
        message = ' ' .join(message.split())
        alarm = {'alarmnumber': alarmnumber, 'category': category, 'keyword': keyword, 'street': street, 'street_addition': street_addition, 'country': country, 'caller': caller, 'message': message}
        return alarm
    except:
        logging.error("unknown error")
        logging.debug("unknown error", exc_info=True)
        return None
