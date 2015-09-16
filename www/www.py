#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 11.05.2015

@author: LZill
'''

from flask import Flask, render_template, redirect
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

from includes import globals

@app.route('/display')
def display():
    conn = sqlite3.connect(globals.database)
    c = conn.cursor()
    c.execute('SELECT * FROM'  + globals.table + 'WHERE address = 1685474 ORDER BY id DESC')
    alarm = c.fetchone()
    conn.close()

    if alarm[11] < str(datetime.now() - timedelta(hours=2)):
        alarm = None
        
    return render_template('display.html', alarm=alarm)
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True)