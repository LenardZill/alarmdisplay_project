#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 20.05.2015

@author: LZill
'''

from flup.server.fcgi import WSGIServer
import view

if __name__ == '__main__':
    WSGIServer(app).run()