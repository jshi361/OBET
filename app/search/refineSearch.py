from datetime import datetime
from flask_paginate import Pagination
from flask import render_template, redirect, url_for, request
from .. import db
from .forms import SearchForm
from mongoengine.queryset.visitor import Q
import json


###################
# Refine List
###################
# Refine the list of search results to those user specifies
def refineList(request, search, page=1):
	default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}
	# If refine list comes from the advanced search
	#if(search == "adv"):

		# Take the data from the request
		#req_form = request.form

		# Save the query
		#formString = req_form['redefinedString']

		# Load the string into a python dict if it exists
		#if formString:
		 	#lit = json.loads(formString)
		#else:
		 	#lit = none

		# Get 'preferences' cookie
		#preferences = request.cookies.get('preferences')

		# If the cookie doesnt exist
		#if not preferences:

			# Return default preferences
			#preferences = default_pref
		#else:

			# Otherwise convert the cookie to a python object
			#preferences = json.loads(preferences)
 		#return render_template('advancedSearch.html', lit = lit, sessioninfo = req_form['queryString'], preferences = preferences)

 	# Otherwise the request is from a the regular search
 	if (search=="reg"):
 		# Save request data
 		req_form = request.form

 		# Create new search form
	 	form = SearchForm()

	 	# Display all values in request for debugging

	 # 	f = request
		# for key in f.keys():
		# 	for value in f.getlist(key):
		# 		print key,":",value

		# Set search term in form to original search term
		form.search.data = req_form['queryString']
		form.sort.data = req_form['sortStr']

		# Save refined json string array of lit
		formString = req_form['redefinedString']

		# Convert the json array into python list
		if formString:
		 	lit = json.loads(formString)
		else:
		 	lit = none

		total = len(lit)

		# Get 'preferences' cookie
		preferences = request.cookies.get('preferences')

		# If the cookie doesnt exist
		if not preferences:

			# Return default preferences
			preferences = default_pref

		else:

			# Otherwise convert the cookie to a python object
			preferences = json.loads(preferences)

		send_lit=[]

		start = page*30-30
		end = page*30

		lastEntry = total

		temp = []

		if total>30 and (total-(page*30-30))>=end:
			for i in range(start, end):
				temp.append(lit[i])
			print(start, " and to ", end)
			print('if more than 30, length of what is left:', len(temp))

			send_lit.extend(temp)

		else:
			for i in range(start, lastEntry):
				temp.append(lit[i])
			print(start, " and to ", lastEntry+1)
			print('length of what is left:', len(temp))

			send_lit.extend(temp)

		pagination = Pagination(
			page=page,
			per_page=30,
			total=total,
			record_name='references'
		)

		return render_template('search.html', form = form, lit = lit, preferences = preferences, total=total, pagination = pagination)
