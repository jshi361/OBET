#################################
# Form definitions as classes
#################################
# Import the Form class and fields wtform
from flask_wtf import Form
from wtforms import SelectField, SubmitField

class BrowseForm(Form):
    sort = SelectField('Sort by: ', choices = [('None',''), ('author', 'Author/Editor'), ('yrPublished', 'Year'), ('title', 'Title'), ('sourceTitle', 'Source Title'), ('primaryField', 'Primary Field'), ('creator', 'Creator'), ('created_date', 'Date Created')])
    submit = SubmitField('Search')
