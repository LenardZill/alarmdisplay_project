#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import MySQLdb

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


@app.route('/')
def show_alarm():
    db = connect_db()
    alarm = []
    if db is not None:
        cur = db.cursor()
        cur.execute('SELECT * FROM alarmitems ORDER BY id WHERE DESC LIMIT 1')

        for row in cur:
            alarm = row
    return render_template('display.html', alarm=alarm)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True)
