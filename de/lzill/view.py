#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 11.05.2015

@author: LZill
'''

from flask import Flask, render_template, redirect
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

# Only on Raspberry
#database = '/var/www/alarmdisplay_project/de/lzill/data/alarmdisplay.db'

# Only on PC
database = 'data/alarmdisplay.db'

@app.route('/display')
def display():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT * FROM alarmitems WHERE address = 1685474 ORDER BY id DESC')
    alarm = c.fetchone()
    conn.close()

    if alarm[11] < str(datetime.now() - timedelta(hours=2)):
        alarm = None
        
    return render_template('display.html', alarm=alarm)

@app.route('/alarmlist')
def alarmlist_all():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT * FROM alarmitems ORDER BY id DESC LIMIT 300')
    alarms = c.fetchall()
    c.execute('SELECT category FROM alarmitems GROUP BY category')
    categories = c.fetchall()
    conn.close()
    return render_template('alarmlist.html', alarms=alarms, categories=categories)

@app.route('/alarmlist/<category>')
def alarmlist_category(category):
    if category <> '-':
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('SELECT * FROM alarmitems WHERE category ="' + category+'"  ORDER BY id DESC LIMIT 300')
        alarms = c.fetchall()
        c.execute('SELECT category FROM alarmitems GROUP BY category')
        categories = c.fetchall()
        conn.close()
        return render_template('alarmlist.html', alarms=alarms, categories=categories)
    else:
        return redirect('/alarmlist')
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True)