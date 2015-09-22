#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import MySQLdb

from flask import Flask, render_template
from datetime import datetime, timedelta
from includes import globals

app = Flask(__name__)

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
    cur = db.cursor()
    for result in cur.excecute('select * from alarmitems where ric=%s order by id desc limit 1',('',)):
        print("Rows produced by statement '{}':".format(result.statement))
        print(result.fetchall())
    else:
        print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True)