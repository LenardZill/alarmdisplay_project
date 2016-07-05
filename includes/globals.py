#!/usr/bin/python
# -*- coding: cp1252 -*-

config = 0
script_path = ''
log_path = ''

doubleList = []
pluginList = {}
filterList = []

ricDescribtionList = {}
keywordDescribtionList = {}


def getvers(mode='vers'):
    if mode == 'vers':
        return '1.5'
    elif mode == 'date':
        return '2016/07/05'
