#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import MySQLdb

from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

def connect_db():
    try:
        connection = MySQLdb.connect(host='localhost',
                                            user='root',
                                            passwd='root',
                                            db='alarmdisplay')
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
        for result in cur.execute('select * from alarmitems worder by id desc limit 1'):
            print("Rows produced by statement '{}':".format(result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
    
    
if __name__ == '__main__':
    show_alarm()
    app.run(host='0.0.0.0', port=88, debug=True)