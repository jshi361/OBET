from flask_paginate import Pagination
from flask import render_template, redirect, url_for, flash, request, make_response
from .forms import BrowseForm
from .functions import litToJson, convertId
from .. import db # Import database model
from ..models import Lit
from mongoengine.queryset.visitor import Q
import json

default_pref = {"author": True, "yrPublished": True, "title":True, "sourceTitle": True, "primaryField": True, "creator": True, "dateCreatedOn": True, "editor": False, "refType": False, "lastModified": False, "lastModifiedBy": False}

def browseForm(request, req_form):
    form = BrowseForm()
    lit = Lit.objects()

    #this sorts the entries using the 'sort by' drop down. if the drop down is not left blank, then sort using specified field.
    if req_form.sort.data and str(req_form.sort.data) != 'None':
        sortStr = str(req_form.sort.data)
        lit = sorted(lit, key=lambda lit:getattr(lit, sortStr))

    # Convert lit to appropiate list object
    jsonlit = litToJson(lit)
    lit = json.loads(jsonlit)
    lit = convertId(lit)

    # Get 'preferences' cookie
    preferences = request.cookies.get('preferences')

    # If the cookie doesnt exist
    if not preferences:
        # Return default preferences
        preferences = default_pref
    else:
        # Otherwise convert the cookie to a python object
        preferences = json.loads(preferences)

    return (form, lit, preferences)
