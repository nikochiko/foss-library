from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

from foss_library.utils import UniqueCheck
from .models import Member

class MemberForm(FlaskForm):
    _model = Member

    name = StringField(validators=[InputRequired()])
    email = EmailField(validators=[InputRequired()])


class CreateMemberForm(MemberForm):
    email = EmailField(validators=[InputRequired(), UniqueCheck()])


class UpdateMemberForm(MemberForm):
    pass
