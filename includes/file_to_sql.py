#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Created on 11.05.2015

@author: LZill
'''

import sqlite3
from datetime import datetime
import urllib2
import os

offlineFile = 'data/169-890M.txt'
onlineFile = 'http://se8sen3y5utitvix.myfritz.net/pager/169-890M.txt'

# Only on Raspberry
database = '/var/www/alarmdisplay_project/de/lzill/data/includes.db'

# Only on PC
#database = 'data/includes.db'

def insertRecord(address, alarmnumber, category, keyword, alarmdate, street, street_addition, country, caller, message):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT id FROM alarmitems WHERE address=?  AND alarmnumber=? AND category=?', (address, alarmnumber, category))
    alarm = c.fetchone()
    if not alarm:
        c.execute('INSERT OR IGNORE INTO alarmitems VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', (None,address, alarmnumber, category, keyword, alarmdate, street, street_addition, country, caller, message, datetime.now()))
        conn.commit()
        print 'insert <' + address + ';' + alarmnumber + ';' + alarmdate + ';' + category + '>'
    conn.close()


def readOfflineFile():
    if (os.path.exists(offlineFile)): 
        response = open(offlineFile, 'r')
        for line in response:
            splitLine(line)
        response.close()
    else:
        print 'offlinefile is not available'


def readOnlineFile():
    response = urllib2.urlopen(onlineFile)
    if response.code == 200:
        for line in response:
            splitLine(line)
    else:
        print 'onlinefile is not available'
        

def splitLine(line):
    try:
        if 'Alpha:   ' in line:
            line = line.split('<NUL>')[0]
            split = line.split('/')
            address = split[0].split(' ')[2].strip()
            alarmnumber = split[0][-6:-1].strip()
            category = split[0][-1:].strip()
            keyword = split[1].split(')')[0].strip()
            alarmdate = datetime.now().strftime('%d.%m.%Y') + ' ' + split[1].split(')')[1].strip()
            street = split[3].replace('(', ' ').replace(')', '').strip()
            street_addition = split[2].split(':')[1].split('(')[0].strip()
            country = split[2].split(':')[0].strip()
            caller = split[2].split('(')[-1].replace(')', '').strip()
              
            message = ''
            messagelist = split[4:]
            for entry in messagelist:
                message += entry.strip() + ' '
            message = message.strip()
            
            address = address.decode('utf-8')
            alarmnumber = alarmnumber.decode('utf-8')
            category = category.decode('utf-8')
            keyword = keyword.decode('utf-8')
            alarmdate = alarmdate.decode('utf-8')
            street = street.decode('utf-8')
            street_addition = street_addition.decode('utf-8')
            country = country.decode('utf-8')
            caller = caller.decode('utf-8')
            message = message.decode('utf-8')
            
            if category == 'B' or category == 'H' or category == 'K' or category == 'P' or category == 'R' or category == 'S' or category == 'T':
                insertRecord(address, alarmnumber, category, keyword, alarmdate, street, street_addition, country, caller, message)
                
    except IndexError:
        pass


if __name__ == '__main__':
    print 'process started <' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '>'
    createTable()
    readOnlineFile()
    print 'process completed <' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '>'
