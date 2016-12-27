from flask.ext.wtf import Form
from wtforms import SubmitField
from wtforms.validators import Required, Length, Optional, NumberRange, URL
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadLitFile(Form):
    file = FileField(
    	'Select File (tsv format)', 
    	validators =[
    		FileRequired(),
    		FileAllowed(['tsv', 'txt'], 'tsv extensions only')
    	])
    submit = SubmitField('Upload File')