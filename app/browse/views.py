##########
# Browse #
##########
from flask_paginate import Pagination
from flask import render_template, redirect, url_for, flash, request, make_response
from flask.ext.session import Session
from . import browse
from .forms import BrowseForm
from .. import db
# Import database model
from ..models import Lit, LitEditRecord
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user
import json

# Default user preferences for search result fields display
default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}


@browse.route('/browse', methods = ['GET', 'POST'])

def browse():

        form = BrowseForm()

    	search = False
    	q = request.args.get('q')
    	if q:
    		search = True

    	total = Lit.objects.count()
    	page = request.args.get('page', type=int, default=1)

    	#start=page*10-10
    	#end=page*10

        #lit = Lit.objects[start:end].order_by('-yrPublished')

        ##### lines 39 to 48 correctly sort the db, however going to the next page undoes the sort. must investigate. ####

        lit=Lit.objects.order_by('-yrPublished')

        if form.sort.data and str(form.sort.data) != 'None':
            sortStr = str(form.sort.data)
            lit = sorted(lit, key=lambda lit:getattr(lit, sortStr))

        i=(page-1)*10
        lit_page=lit[i:i+10]

    	preferences = request.cookies.get('preferences')
    	if not preferences:
     		# Return default preferences
     		preferences = default_pref
     	else:
     		# Otherwise convert the cookie to a python object
     		preferences = json.loads(preferences)

        pagination = Pagination(
            page=page,
    		per_page=10,
    		total=total,
    		search=search,
    		record_name='references'
    	)

    	return render_template(
    		'browse.html',
        	lit = lit_page,
        	pagination = pagination,
        	total=total,
        	preferences = preferences,
            form = form
        	)
