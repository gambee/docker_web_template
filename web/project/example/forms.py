from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, widgets
from wtforms.validators import DataRequired, Regexp
import re

class Example_Form(FlaskForm):
    some_text = StringField(
            'Some Text',
            validators=[
                DataRequired(message='Some Text is Required')
            ])
