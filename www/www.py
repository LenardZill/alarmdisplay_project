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
        cur.execute('SELECT * FROM alarmitems WHERE ric=%s ORDER BY id DESC LIMIT 1',('1694418'))
        
        for row in cur:
            print(row)
    
    
if __name__ == '__main__':
    show_alarm()
    app.run(host='0.0.0.0', port=88, debug=True)