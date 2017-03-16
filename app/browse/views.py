##########
# Browse #
##########
from flask_paginate import Pagination
from flask_session import Session
from flask import render_template, redirect, url_for, flash, request, make_response, session
from . import browse
from .forms import BrowseForm
from .browseForm import browseForm
from .. import db
# Import database model
from ..models import Lit, LitEditRecord
from mongoengine.queryset.visitor import Q
from flask_login import login_required, current_user
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

    total= Lit.objects.count()

    # if a POST request is made: get form, lit and preferences returned in browseForm
    # store lit and preferences in session variables
    if request.method == 'POST':
        form, lit, preferences = browseForm(request, form)
        session['lit'] = lit
        session['preferences'] = preferences
        page = request.args.get('page', type=int, default=1)

    # if a GET request is made: check if there are lit and preferences sessions, if so use them
    if request.method == 'GET':
        if 'lit' in session:
            lit = session.get('lit')
        else:
            lit = Lit.objects.order_by('-yrPublished')
        if 'preferences' in session:
            preferences = session.get('preferences')
        else:
            preferences = default_pref
        page = request.args.get('page', type=int, default=1)
    else:
        page=1

    # allowing 30 entries per page
    i=(page-1)*30
    lit_page=lit[i:i+30]

    pagination = Pagination(
        page=page,
        per_page=30,
        total=total,
        search=search,
        record_name='references'
    )

    return render_template(
        'browse.html',
        lit = lit_page,
        pagination = pagination,
        total = total,
        preferences = preferences,
        form = form
    )
