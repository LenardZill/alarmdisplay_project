#!/usr/bin/python
# -*- coding: cp1252 -*-

import logging
import csv
from includes import globals


def load_csv(typ, idField):
	resultList = {}
	try:
		logging.debug("-- loading %s.csv", typ)
		with open(globals.script_path+'/csv/'+typ+'.csv') as csvfile:
			# DictReader expected structure described in first line of csv-file
			reader = csv.DictReader(csvfile)
			for row in reader:
				logging.debug(row)
				# only import rows with an integer as id
				if row[idField].isdigit():
					resultList[row[idField]] = row['description']
		logging.debug("-- loading csv finished")
	except:
		logging.error("loading csvList for typ: %s failed", typ)
		logging.debug("loading csvList for typ: %s failed", typ, exc_info=True)
		raise
	return resultList;


def load_description_list():
    try:
        logging.debug('loading description list')

        if globals.config.getint('POC', 'idDescribed'):
            logging.debug('- load pocsag description list')
            globals.ricDescribtionList = load_csv('poc', 'ric')
    except:
        logging.error("cannot load description lists")
        logging.debug("cannot load description lists", exc_info=True)
        pass


def get_description(typ, id):
	resultStr = id;
	logging.debug("look up description lists")
	try:
		if typ == "POC":
			resultStr = globals.ricDescribtionList[id]
		else:
			logging.warning("Invalid Typ: %s", typ)

	except KeyError:
		pass

	except:
		logging.error("Error during look up description lists")
		logging.debug("Error during look up description lists", exc_info=True)
		pass

	logging.debug(" - result for %s: %s", id, resultStr)
	return resultStr
