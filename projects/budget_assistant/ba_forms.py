from wtforms import Form, BooleanField, StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo 
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

class uploadForm(FlaskForm):

    file = FileField(
        'Upload Bank Statement',
        validators=[
            FileRequired(),
            FileAllowed(['csv'], 'Only CSV files are allowed.')
        ]
    )
    bank_selection = SelectField('Select Bank', choices=[
        ('UBS', 'UBS')
        # Add more banks as needed
    ])