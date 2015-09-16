#!/usr/bin/python
# -*- coding: cp1252 -*-

from Tkinter import *
from time import sleep    
import logging

main = Tk()
test = StringVar()


def onload():
    try:
        test.set('testvariable')
        w, h = main.winfo_screenwidth(), main.winfo_screenheight()
        main.overrideredirect(1)
        main.geometry('%dx%d+0+0' % (w, h))
        main.focus_set()
        main.bind('<Escape>', lambda e: e.widget.quit())
        Label(main,
              textvariable=test,
              font='Arial 10').pack()
        main.mainloop()
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
        raise


def run(typ, freq, data):
    try:
        sleep(1)
        test.set(data['msg'])
        main.update_idletasks()
    except:
        logging.error('unknown error')
        logging.debug('unknown error', exc_info=True)
