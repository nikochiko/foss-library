from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange, Optional


class ImportDataForm(FlaskForm):
    count = IntegerField(validators=[InputRequired(), NumberRange(min=1)])
    title = StringField(validators=[Optional()])
    authors = StringField(validators=[Optional()])
    isbn = StringField(validators=[Optional(), Length(min=10, max=10)])
    publisher = StringField(validators=[Optional()])
