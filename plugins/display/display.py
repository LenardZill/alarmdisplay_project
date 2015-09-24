#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import MySQLdb

from flask import Flask, render_template
from includes import globals

app = Flask(__name__)

def onload():
    app.run(host='0.0.0.0', port=88, debug=True)

def connect_db():
    try:
        connection = MySQLdb.connect(host=globals.config.get('MySQL', 'dbserver'),
                                         user=globals.config.get('MySQL', 'dbuser'),
                                         passwd=globals.config.get('MySQL', 'dbpassword'),
                                         db=globals.config.get('MySQL', 'database'))
        return connection
    except:
        logging.error('cannot connect to MySQL')
        logging.debug('cannot connect to MySQL', exc_info=True)
        return
    
@app.route('/')
def show_alarm():
    db = connect_db()
    if db is not None:
        cur = db.cursor()
        cur.execute('SELECT * FROM alarmitems ORDER BY id DESC LIMIT 1')
        
        for row in cur:
            alarm = row
            print(row)
    else:
        alarm = ["1","2015-09-16 09:15","169447","1","a","09263R/chir. Notfall) 16:16/Schoenningstedt:Bismarck Seniorenstift(Schmanz)/Muehlenweg(8 -10)//Koplawu","12000","1694474","09263","B","Feuer Gross","Trittauer Strasse 15","", "Grossensee", "", "Brennt Gebauude ca 200 Quadratmeter"]
    return render_template('display.html', alarm=alarm)