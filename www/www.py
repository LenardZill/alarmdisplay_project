#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
#import MySQLdb

from flask import Flask, render_template

from includes import globals

app = Flask(__name__)

def connect_db():
    try:
        connection = MySQLdb.connect(host='localhost',
                                     user='root',
                                     passwd='root',
                                     db='alarmdisplay',
                                     use_unicode=True)
        return connection
    except:
        logging.error('cannot connect to MySQL')
        logging.debug('cannot connect to MySQL', exc_info=True)
        return

def get_alarms():
    db = connect_db()
    rows = []
    if db is not None:
        cur = db.cursor()
        cur.excecute('SELECT time, ric, alarmnumber, category, keyword, street, street_addition, country, caller, message FROM alarmitems ORDER BY id DESC LIMIT 10')
        rows = cur.fetchall()
        
    return rows


def get_alarm():
    db = connect_db()
    row = []
    if db is not None:
        cur = db.cursor()
        cur.excecute('SELECT time, ric, alarmnumber, category, keyword, street, street_addition, country, caller, message FROM alarmitems ORDER BY id DESC LIMIT 1')
        row = cur.fetchone()
        
    return row
    

@app.route('/')
def show_alarm():
    
    #alarm = []
    alarm = ["29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"]
    alarms = [("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"), 
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"), 
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
              ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung")]
    
    alarm = get_alarm()
    alarms = get_alarms()
    
    return render_template('display.html', alarm=alarm, alarms=alarms)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True)
