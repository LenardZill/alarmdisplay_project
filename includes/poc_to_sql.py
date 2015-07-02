#!/usr/bin/python
# -*- coding: cp1252 -*-

'''
Created on 29.06.2015

@author: LZill
'''

import time
import subprocess
import os
import sqlite3

database = '/var/www/alarmdisplay_project/de/lzill/data/includes.db'

try:
    connection = sqlite3.connect(database)
    connection.close()
except:
    print 'Keine Verbindung zur Datenbank'
    exit(0)
    
def curtime():
    return time.strftime("%Y-%m-%d %H:%M:%S")

with open('data/fehler.txt', 'a') as errorfile:
    errorfile.write(('#' * 20) + '\n' + curtime() + '\n')
    
multimon_ng = subprocess.Popen("rtl_fm -f 169.890M -M fm -s 22050 -p 37 -E DC -F 0 -1 -g 100",
                               #stdin=rtl_fm.stdout,
                               stdout=subprocess.PIPE,
                               stderr=open('error.txt','a'),
                               shell=True)

try:
    while True:
        line = multimon_ng.stdout.readline()
        multimon_ng.poll()
        if line.__contains__("Alpha:"):
            if line.startswith('POCSAG'):
                address = line[21:28].replace(" ", "")
                subric = line[40:41].replace(" ", "").replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
                message = line.split('Alpha:   ')[1].strip().rstrip('').strip()
                output=(curtime()+' '+ address+' '+ subric+' '+ message+'\n')
                print curtime(), address, subric, message
                with open('data/POCSAG.txt','a') as f:
                    f.write(output)
                connection = sqlite3.connect(database)
                c = connection.cursor()
                c.excecute('')
                connection.commit()
                connection.close()
                
                # Hier import in Datenbank realisieren...
        if not "Alpha:" in line:
            with open("data/POCSAG_KeinText.txt","a") as missed:
                address = line[21:28].replace(" ", "")
                subric = line[40:41].replace(" ", "").replace("3", "4").replace("2", "3").replace("1", "2").replace("0", "1")
                print  curtime(), address, sum
                missed.write(line)
                connection = sqlite3.connect(database)
                c = connection.cursor()
                c.excecute('')
                connection.commit()
                connection.close()
                
except KeyboardInterrupt:
    os.kill(multimon_ng.pid, 9)
        
                 
                
                
                