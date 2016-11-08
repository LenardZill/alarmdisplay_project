#!/usr/bin/python
# -*- coding: cp1252 -*-

from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)


@app.route('/get_alarm')
def get_alarm():
        f = open('U:/My Documents/Entwicklung/alarmdisplay_project/data/alarms.txt', 'r')
        lines = f.readlines()
        f.close()

        if len(lines) > 0:
            data = lines[-1].split(';')
            return jsonify(alarmid=data[0], keyword=data[1], keyword_desc=data[5] + ' (' + data[4] + ')', date=data[2], fire_stations=data[8], message=data[6], info=data[7])
        else:
            return jsonify(alarmid='', keyword='', keyword_desc='', date='', fire_stations='', message='Kein Einsatz vorhanden!', info='')


@app.route('/accept_alarm/<alarmid>/', methods=['POST'])
def accept_alarm(alarmid):
    if alarmid:
        os.rename('U:/My Documents/Entwicklung/alarmdisplay_project/data/alarms.txt',
                  'U:/My Documents/Entwicklung/alarmdisplay_project/data/alarms.old.txt')
        with open('U:/My Documents/Entwicklung/alarmdisplay_project/data/alarms.old.txt') as oldfile, \
                open('U:/My Documents/Entwicklung/alarmdisplay_project/data/alarms.txt', 'w') as newfile:
            for line in oldfile:
                if not alarmid + ';' in line:
                    newfile.write(line)
        os.remove('U:/My Documents/Entwicklung/alarmdisplay_project/data/alarms.old.txt')
    return alarmid

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=True)
