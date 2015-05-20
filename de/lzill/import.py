#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 11.05.2015

@author: LZill
'''

import sqlite3
import datetime, time
import urllib2
import os


# Only on Raspberry
database = '/var/www/alarmdisplay_project/de/lzill/data/alarmdisplay.db'
offlineFile = '/var/www/alarmdisplay_project/de/lzill/data/169-890M.txt'
onlineFile = 'http://se8sen3y5utitvix.myfritz.net/pager/169-890M.txt'

# Only on PC
#database = 'data/alarmdisplay.db'
#offlineFile = 'data/169-890M.txt'
#onlineFile = 'http://se8sen3y5utitvix.myfritz.net/pager/169-890M.txt'

def createTable():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    conn.text_factory = str
    c.execute('''CREATE TABLE IF NOT EXISTS alarmitems
                (id INTEGER PRIMARY KEY, address TEXT, alarmnumber TEXT, category TEXT, keyword TEXT, alarmdate TEXT, 
                street TEXT, street_addition TEXT, country TEXT, caller TEXT, message TEXT, created_at DATETIME)''')
    conn.commit()
    conn.close()
    
    
def removeEntrys(limit):
    conn = sqlite3.connect(database)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('DELETE FROM alarmitems WHERE id NOT IN (SELECT id FROM alarmitems ORDER BY id ASC LIMIT ?)', (limit))
    conn.commit()
    conn.close()
    print 'the latest ' + limit + ' records were removed'


def insertRecord(address, alarmnumber, category, keyword, alarmdate, street, street_addition, country, caller, message):
    conn = sqlite3.connect(database)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('SELECT id FROM alarmitems WHERE address=?  AND alarmnumber=? AND category=?', (address, alarmnumber, category))
    alarm = c.fetchone()
    if not alarm:
        c.execute('INSERT OR IGNORE INTO alarmitems VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', (None,address, alarmnumber, category, keyword, alarmdate, street, street_addition, country, caller, message, datetime.datetime.now()))
        conn.commit()
        print 'insert <' + address + ';' + alarmdate + ';' + category + ';' + keyword +  ';' + message + '>'
    conn.close()
    
def rowCount():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT COALESCE(MAX(id)+1, 0) FROM alarmitems')
    print c.fetchone()
    conn.close

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
            alarmdate = split[1].split(')')[1].strip()
            street = split[3].replace('(', ' ').replace(')', '').strip()
            street_addition = split[2].split(':')[1].split('(')[0].strip()
            country = split[2].split(':')[0].strip()
            caller = split[2].split('(')[-1].replace(')', '').strip()
            
            message = ''
            messagelist = split[4:]
            for entry in messagelist:
                message += entry.strip() + ' '
            message = message.strip()
            
            insertRecord(address, alarmnumber, category, keyword, alarmdate, street, street_addition, country, caller, message)
    except IndexError:
        pass


if __name__ == '__main__':
    print 'process started <' + time.strftime("%Y-%m-%d %H:%M:%S") + '>'
    createTable()
    readOnlineFile()
    #readOfflineFile()
    print 'process completed <' + time.strftime("%Y-%m-%d %H:%M:%S") + '>'