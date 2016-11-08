#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import csv
from includes import globals
import re


def load_csv():
	resultList = {}
	try:
		logging.debug("-- loading keywords.csv")
		with open(globals.script_path+'/csv/keywords.csv') as csvfile:
			# DictReader expected structure described in first line of csv-file
			reader = csv.DictReader(csvfile)
			for row in reader:
				logging.debug(row)
				
				resultList[row['keyword']] = row['description'], row['type']
		logging.debug("-- loading csv finished")
	except:
		logging.error("loading keywordList failed")
		logging.debug("loading keywordList failed", exc_info=True)
		raise
	return resultList;


def load_description_list():
	try:
		logging.debug('loading description list')
		
		if globals.config.getint('POC', 'keywordDescribed'):
			logging.debug('- load keyword description list')
			globals.keywordDescribtionList = load_csv()
	except:
		logging.error("cannot load keyword description lists")
		logging.debug("cannot load keyword description lists", exc_info=True)
	pass


def get_description(keyword):
	resultStr = '' #keyword
	logging.debug("look up keyword description lists")
	try:
		keys = re.sub('(?<!\d)\d{2}(?!\d)', '', keyword).split(' ')
		addition = {'AUS', 'K', 'G','2', '3', '4', '5', '6', '7', 'WAL'}
		
		list = []
		for key in keys:
			if key in addition:
				list[-1] = list[-1] + ' ' + key
			else:
				list.append(key)

		for key in list:
			resultStr += ' ' + globals.keywordDescribtionList[key][0]

		resultStr += ' (' + keyword + ')'
	except KeyError:
		pass

	except:
		logging.error("Error during look up keyword description lists")
		logging.debug("Error during look up keyword description lists", exc_info=True)
		pass

	logging.debug(" - result for %s: %s", keyword, resultStr)
	return resultStr
