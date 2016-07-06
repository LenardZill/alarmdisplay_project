#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import MySQLdb
from flask import Flask, render_template

app = Flask(__name__)

debug = True

alarm_ric = 1685474
ric_list = [1684978, 1685474, 1685402, 1685330, 1685186, 1685258, 1685618]


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


def get_alarm():
    alarm = None
    if debug:
        alarm = ["29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"]
    else:
        db = connect_db()
        if db is not None:
            cur = db.cursor()
            cur.excecute('SELECT time, ric, alarmnumber, category, keyword, street, street_addition, country, caller, message FROM alarmitems WHERE ric=' + alarm_ric + ' AND time BETWEEN DATE_SUB(NOW() , INTERVAL 3 HOUR) AND NOW() ORDER BY id DESC LIMIT 1')
            alarm = cur.fetchone()
    return alarm


def get_recend_alarm_list():
    recend_alarm_list = None
    if debug:
        recend_alarm_list = [("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
                            ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
                            ("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung")]
    else:
        db = connect_db()
        if db is not None:
            cur = db.cursor()
            cur.excecute('SELECT time, ric, alarmnumber, category, keyword, street, street_addition, country, caller, message FROM alarmitems WHERE ric=' + alarm_ric + ' ORDER by id DESC LIMIT 5')
            recend_alarm_list = cur.fetchall()
    return recend_alarm_list
  
    
def get_alarm_list():
    alarm_list = None
    if debug:
        alarm_list = [("29.10.2015 08:47", "11111", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"), 
                      ("29.10.2015 08:47", "22222", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"), 
                      ("29.10.2015 08:47", "33333", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
                      ("29.10.2015 08:47", "44444", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),
                      ("29.10.2015 08:47", "55555", "1", "T", "Testeinsatz", "Musterstrasse", "Strassenzusatz", "Grande", "Max Mustermann", "Testalarmmeldung"),]
    else:
        db = connect_db()
        if db is not None:
            cur = db.cursor()
            cur.excecute('SELECT time, ric, alarmnumber, category, keyword, street, street_addition, country, caller, message FROM alarmitems WHERE ric=' + ' OR ric='.join([str(x) for x in ric_list]) + ' ORDER BY id DESC LIMIT 5')
            alarm_list = cur.fetchall()
    return alarm_list


@app.route('/alt/')
def index_alt():
    alarm = get_alarm()
    recend_alarm_list = get_recend_alarm_list()
    alarm_list = get_alarm_list()
    
    if alarm:
        return render_template('display.html', alarm=alarm)
    else:
        return render_template('idle.html', alarm_list=alarm_list, recend_alarm_list=recend_alarm_list)


@app.route('/alt/display')  
def display_alt():
    alarm = get_alarm()
    return render_template('display.html', alarm=alarm)


@app.route('/alt/idle')
def idle_alt():
    recend_alarm_list = get_recend_alarm_list()
    alarm_list = get_alarm_list()
    return render_template('idle.html', alarm_list=alarm_list, recend_alarm_list=recend_alarm_list)


@app.route('/')
def display():
    alarm = get_alarm()
    
    return render_template('idle.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True)