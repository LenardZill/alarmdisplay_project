#!/usr/bin/python
# -*- coding: cp1252 -*-

config = 0
script_path = ''
log_path = ''

doubleList = []
pluginList = {}
filterList = []

ricDescribtionList = {}


def getvers(mode='vers'):
    if mode == 'vers':
        return '1.0'
    elif mode == 'date':
        return '2015/09/16'
