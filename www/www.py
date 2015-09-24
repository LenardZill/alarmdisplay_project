#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import MySQLdb

from flask import Flask, render_template

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
    
def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"    

@app.route('/')
def show_alarm():
    db = connect_db()
    alarm = []
    if db is not None:
        cur = db.cursor()
        cur.execute('SELECT * FROM alarmitems WHERE 1=2 ORDER BY id DESC LIMIT 1')
        
        for row in cur:
            alarm = row
    else:
        alarm = ["1","2015-09-16 09:15","169447","1","a","09263R/chir. Notfall) 16:16/Schoenningstedt:Bismarck Seniorenstift(Schmanz)/Muehlenweg(8 -10)//Koplawu","12000","1694474","09263","B","Feuer Gross","Trittauer Strasse 15","", "Grossensee", "", "Brennt Gebauude ca 200 Quadratmeter"]
    return render_template('display.html', alarm=alarm)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True) 