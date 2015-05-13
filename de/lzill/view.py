#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 11.05.2015

@author: LZill
'''

from flask import Flask, render_template, redirect, escape
import sqlite3

app = Flask(__name__)

database = 'data/alarmdisplay.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT * FROM alarmitems ORDER BY id DESC')
    alarm = c.fetchone()
    conn.close()
    
    return render_template('display.html', alarm=alarm)

@app.route('/alarmlist')
def alarmlist_all():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT * FROM alarmitems ORDER BY id DESC')
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
        c.execute('SELECT * FROM alarmitems WHERE category ="' + category+'"  ORDER BY id DESC')
        alarms = c.fetchall()
        c.execute('SELECT category FROM alarmitems GROUP BY category')
        categories = c.fetchall()
        conn.close()
        return render_template('alarmlist.html', alarms=alarms, categories=categories)
    else:
        return redirect('/alarmlist')
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)