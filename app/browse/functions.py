from datetime import datetime
#from flask_paginate import Paginate
from flask import render_template, redirect, url_for, flash, request, make_response
from .. import db # Import database model
from ..models import Lit
from mongoengine.queryset.visitor import Q
import json, cgi, csv, io, collections

# Utility function
def litToJson(lit):
	# Create a json string of lit
	jsonlit = '['
	for literature in iter(lit):
		jsonlit+= ( literature.to_json() + ", ")
	# Remove the last comma and space
	if len(jsonlit) > 7:
		jsonlit = jsonlit[:-2]
	jsonlit += "]"
	return jsonlit

# Utility function to convert lit object into string
def convertId(lit):
	for l in lit:
		# Convert id to basic string id
		litid = "%s" % l["_id"]
		litid = litid.replace("{u'$oid': u'", "")
		litid = litid.replace("'}", "")
		l["id"] = litid

		# Convert date to basic date
		litdate = "%s" % l["created_date"]
		litdate = litdate.replace("{u'$date': ", "")
		litdate = litdate.replace("L", "")
		litdate = int(litdate.replace("}", ""))
		litdate = litdate/1000.0
		litdate = str(datetime.fromtimestamp(litdate).strftime('%Y-%m-%d %H:%M:%S'))
		l["created_date"] = litdate

		# Convert date to basic date
		if("last_edit" in l.keys()):
			litdate = "%s" % l["last_edit"]["date"]
			litdate = litdate.replace("{u'$date': ", "")
			litdate = litdate.replace("L", "")
			litdate = int(litdate.replace("}", ""))
			litdate = litdate/1000.0
			litdate = str(datetime.fromtimestamp(litdate).strftime('%Y-%m-%d %H:%M:%S'))
			l["last_edit"]["date"] = litdate

	return lit
