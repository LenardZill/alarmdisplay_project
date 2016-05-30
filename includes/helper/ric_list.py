#!/usr/bin/python
# -*- coding: cp1252 -*-

__author__ = 'LenardZill'


def decode_ric(ric):
    if ric == '1684978':
        return 'FF Trittau'
    elif ric == '1685474':
        return 'FF Grande'
    elif ric == '1685402':
        return 'FF Witzhave'
    elif ric == '1685330':
        return 'FF Rausdorf'
    elif ric == '1685186':
        return 'FF Lütjensee'
    elif ric == '1685258':
        return 'FF Großensee'
    elif ric == '1685618':
        return 'FF Köthel'
    else:
        return ''