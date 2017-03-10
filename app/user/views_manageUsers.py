from flask_paginate import Pagination
from flask import url_for, render_template, flash, redirect, request
from . import user
from .. import db
from .forms import DeleteUserForm, UpdateUserRole
from mongoengine.queryset.visitor import Q
from flask_login import login_required, current_user
from ..decorators import admin_required
from ..models import User

###############
# Delete User #
###############
## Does not work the way we want, yet.

@user.route('/manageUsers', methods=['GET', 'POST'])
@login_required
@admin_required
def manageUsers():
	users = User.objects().order_by('-role', 'name')
	total = User.objects.count()
	page = request.args.get('page', type=int, default=1)
	start=page*30-30
	end=page*30
	pagination = Pagination(
		page=page,
		per_page=30,
		total=total,
		record_name='users'
	)

 	form = DeleteUserForm()
 	roleForm = UpdateUserRole()
 	if roleForm.submitRole.data and roleForm.validate_on_submit():
 		role_update = roleForm.role.data
		user = User.objects(email__iexact = roleForm.email.data).first()
		print(role_update)
 		if user is None:
 			flash("No user like this in the database.")
 		if role_update == None:
 			flash("Please select a role.")
	 	if user != None:
	 		current = user.role.name
	 		if current == 'Administrator':
	 			if role_update == 'Administrator':
	 				flash("User is already an Administrator.")
	 			else:
	 				user.set_as_user()
	 				flash("User is now a user")
	 		if current == 'User':
	 			if role_update == 'Administrator':
	 				user.set_as_ad()
	 				flash("User is now an administrator.")
	 			else:
	 				flash("User is already a User.")
 		return redirect(url_for('user.manageUsers'))
 	if form.submit.data and form.validate_on_submit():
		user = User.objects(email__iexact = form.email.data).first()
		if user is None:
 			flash("No user like this in the database.")
 		else:
 			user.delete()
 			flash("User deleted.")
 		return redirect(url_for('user.manageUsers'))
 	return render_template(
 		'manageUsers.html',
 		form = form,
 		pagination = pagination,
    	total=total,
    	users = users,
    	roleForm = roleForm
    	)
