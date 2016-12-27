from werkzeug.utils import secure_filename
from datetime import datetime
#from flask_paginate import Paginate
from flask import render_template, redirect, url_for, flash
from . import lit
from .forms import AddLitForm, UploadLitFile
from .. import db
# Import database model
from ..models import Lit, LitEditRecord, UserEditRecord
from mongoengine.queryset.visitor import Q
from flask.ext.login import login_required, current_user
###########
# Add Lit #
###########

# Add literature
@lit.route('/addLit', methods=['GET', 'POST'])
@login_required
def addLit():
 	total = 0
 	count = 0
	# Add form for file upload
	formFile = UploadLitFile()
	# Create new add lit form
 	form = AddLitForm()

 	if formFile.submit.data and formFile.validate_on_submit():
		if formFile.file.data.filename == '':
				flash('No Selected File')
		else:
			filename = secure_filename(formFile.file.data.filename)
			file = formFile.file.data
			flash('File uploaded. Processed')
			read = file.readlines()
			lines = read[0].split('\r')
			total = len(lines)-1
			print('total', total)
			count = 0
			for line in lines[1:]:
				if count == total:
					break
				entry = line.split('\t')
				print(len(entry))
				lit = Lit.objects(refType__iexact = entry[0], title__iexact = entry[2]).first()
				if lit is not None: 
					flash("This entry is already in the database.")
				else:
					count=count+1
					print(str(entry[12]))
					for x in range(0,17):
						entry[x].strip()
					lit = Lit(refType = entry[0], author = entry[1], title = entry[2], pages = entry[10], primaryField = entry[14], creator = current_user.name)
					lit.save()
					lit.update(set__yrPublished = entry[3])
					lit.update(set__sourceTitle = entry[4])
					lit.update(set__editor = entry[5])
					lit.update(set__placePublished = entry[6])
					lit.update(set__publisher = entry[7])
					lit.update(set__volume = entry[8])
					lit.update(set__number = entry[9])
					lit.update(set__abstract = entry[12])
					lit.update(set__notes = entry[13])
					lit.update(set__secondaryField = entry[15])
					lit.update(set__DOI = entry[17])
					
					# If the link field is not empty, save the link too
					# If statement is done because update fails when attempting to save an empty string
					if form.link.data is not None:
						lit.update(set__link = entry[16])

					# Add keywords into the db as a listField
					keywordslist = entry[11].split(",")
					for x in range(0, len(keywordslist)):
						key = str(keywordslist[x].strip())
						lit.update(push__keywords = key)

					editHist = LitEditRecord(lastUserEdited = current_user.name)
					# Update lit history
					lit.update(push__l_edit_record=editHist)
					lit.update(set__last_edit = editHist)
					lit.reload()

					# Update user edit history
					userHist = UserEditRecord(litEdited = str(lit.id), operation = "add", litEditedTitle = lit.title)
					current_user.update(push__u_edit_record = userHist)
					current_user.reload()
			flash("Successfully added!")
			return redirect(url_for('lit.addLit'))
	else:
		filename = None

 	# On form submission
 	if form.submit.data and form.validate_on_submit():

 		# If the literature is already in the database, then do not add the material, return
		lit = Lit.objects(title__iexact = form.title.data, author__iexact = form.author.data, pages__iexact = form.pages.data).first()
		if lit is not None:
 			flash("This is already in the DB. This is the page")
			return render_template('lit.html', lit = lit)

		# Create a new lit object, save to db first, then update fields
		lit = Lit(refType = form.refType.data, title = form.title.data, pages = form.pages.data, author = form.author.data, primaryField = form.primaryField.data, creator = current_user.name)
		lit.save()
		lit.update(set__yrPublished = form.yrPublished.data)
		lit.update(set__sourceTitle = form.sourceTitle.data)
		lit.update(set__editor = form.editor.data)
		lit.update(set__placePublished = form.placePublished.data)
		lit.update(set__publisher = form.publisher.data)
		lit.update(set__volume = form.volume.data)
		lit.update(set__number = form.number.data)
		lit.update(set__abstract = form.abstract.data)
		lit.update(set__notes = form.notes.data)
		lit.update(set__secondaryField = form.secondaryField.data)

		# Add user's edit in edit history
		editHist = LitEditRecord(lastUserEdited = current_user.name)

		# If the link field is not empty, save the link too
		# If statement is done because update fails when attempting to save an empty string
		if form.link.data is not None:
			lit.update(set__link = form.link.data)

		# Add keywords into the db as a listField
		keywordslist = (form.keywords.data).split(",")
		for x in range(0, len(keywordslist)):
			key = str(keywordslist[x].strip())
			lit.update(push__keywords = key)

		# Update lit history
		lit.update(push__l_edit_record=editHist)
		lit.update(set__last_edit = editHist)
		lit.reload()

		# Update user edit history
		userHist = UserEditRecord(litEdited = str(lit.id), operation = "add", litEditedTitle = lit.title)
		current_user.update(push__u_edit_record = userHist)
		current_user.reload()

		flash("Successfully added!")
 		return redirect(url_for('lit.lit', lit_id = lit.id))
 	return render_template('addLit.html', form = form, formFile = formFile, filename = filename, total = total, count = count)
