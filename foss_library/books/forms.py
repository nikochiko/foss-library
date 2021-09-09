from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, IntegerField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, NumberRange, Optional

from foss_library.utils import UniqueCheck
from .models import Book


class BookForm(FlaskForm):
    _model = Book

    title = StringField("Title", validators=[InputRequired()])
    authors = StringField("Authors", validators=[InputRequired()])
    language_code = StringField(validators=[Optional(), Length(max=7)])
    num_pages = IntegerField(validators=[InputRequired(), NumberRange(min=0)])
    publication_date = DateField(validators=[InputRequired()])
    publisher_name = StringField(validators=[InputRequired()])
    average_rating = DecimalField(validators=[Optional(), NumberRange(min=0, max=5)])
    ratings_count = IntegerField(validators=[Optional(), NumberRange(min=0)])
    text_reviews_count = IntegerField(validators=[Optional(), NumberRange(min=0)])
    total_stock = IntegerField(default=1, validators=[InputRequired(), NumberRange(min=0)])
    rent_per_day = IntegerField(default=1, validators=[Optional(), NumberRange(min=0)])


class CreateBookForm(BookForm):
    isbn = StringField("ISBN 10", validators=[InputRequired(), Length(min=10, max=10), UniqueCheck()])
    isbn13 = StringField("ISBN 13", validators=[InputRequired(), Length(min=13, max=13), UniqueCheck()])


class UpdateBookForm(BookForm):
    isbn = StringField("ISBN 10", validators=[InputRequired(), Length(min=10, max=10)])
    isbn13 = StringField("ISBN 13", validators=[InputRequired(), Length(min=13, max=13)])


class IssueBookForm(FlaskForm):
    member_id = IntegerField(validators=[InputRequired()])


class InitiateBookReturnForm(FlaskForm):
    member_id = IntegerField(validators=[InputRequired()])
