from datetime import datetime
from flask_paginate import Pagination
from flask import render_template, redirect, url_for, flash, request
from . import lit
from .forms import DeleteLitForm
from .. import db
# Import database model
from ..models import Lit, UserEditRecord
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user

# Not currently in use ##############################################################

#################################
# Delete Lit Main Page Function #
#################################
from ..decorators import admin_required, permission_required, user_required
@lit.route('/deleteLit', methods=['GET', 'POST'])
@login_required

def deleteLit():
	default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}

	preferences = request.cookies.get('preferences')
	if not preferences:
 		# Return default preferences
 		preferences = default_pref
 	else:
 		# Otherwise convert the cookie to a python object
 		preferences = json.loads(preferences)
	if current_user.role.name == 'User':
		lit_stored = Lit.objects(creator__exact = current_user.name).order_by('title')
		total = lit_stored.count()
		search = False
		q = request.args.get('q')
		if q:
			search = True
		page = request.args.get('page', type=int, default=1)
		start=page*30-30
		end=page*30
		lit_showed = lit_stored[start:end]
		pagination = Pagination(
			page=page, 
			per_page=30,
			total=total,
			record_name='resources'
		)
	else: 
		total = 0
		lit_showed = None
		page = request.args.get('page', type=int, default=1)
		pagination = Pagination(
			page=page, 
			per_page=30,
			total=total,
			record_name='resources'
		)

 	form = DeleteLitForm()
 	if form.validate_on_submit():
		title = form.title.data.strip()
		refType = form.refType.data.strip()
		lit = Lit.objects(title__exact = title, refType__exact = refType).first()
		if lit is None:
			flash ("No literature like this in the database")
		if current_user.role.name == 'User' and lit.creator != current_user.name:
			flash ('You did not upload this literature. Please delete a literature you uploaded.')
		else:
			userHist = UserEditRecord(litEdited = str(lit.id), litEditedTitle = lit.title, operation = "delete")
			current_user.update(push__u_edit_record=userHist)
			current_user.reload()
			lit.delete()
			flash("Literature has been deleted!")
 		return redirect(url_for('lit.deleteLit'))
 	return render_template('deleteLit.html', form = form, lit_showed = lit_showed, pagination = pagination,
    	total=total, preferences = preferences)

