from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange


class BookForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    isbn = StringField("isbn", validators=[Length(min=10, max=10)])
    isbn13 = StringField("isbn", validators=[DataRequired(), Length(min=13, max=13)])
    authors = StringField("authors", validators=[DataRequired()])
    language_code = StringField(validators=[Length(max=7)])
    num_pages = IntegerField(validators=[DataRequired(), NumberRange(min=0)])
    publication_date = DateField(validators=[DataRequired()])
    publisher_name = StringField(validators=[DataRequired()])
    average_rating = DecimalField(validators=[NumberRange(min=0, max=5)])
    ratings_count = IntegerField(validators=[NumberRange(min=0)])
    text_reviews_count = IntegerField(validators=[NumberRange(min=0)])
    total_stock = IntegerField(validators=[DataRequired(), NumberRange(min=0)])
    rent_per_day = IntegerField(validators=[NumberRange(min=0)])
