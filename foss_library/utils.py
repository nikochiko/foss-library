from flask import flash
from wtforms.validators import ValidationError


class UniqueCheck:
    def __init__(self, message=None):
        if not message:
            message = "%(modelname)s with %(fieldname)s %(fieldvalue)s already exists"

        self.message = message

    def __call__(self, form, field):
        if not hasattr(form, "_model"):
            raise Exception("Expected form to have a _model attribute")

        if form._model.query.filter_by(**{field.name: field.data}).limit(1).count() == 1:
            message = self.message % {
                "modelname": form._model.__name__,
                "fieldname": field.label.text,
                "fieldvalue": field.data,
            }
            raise ValidationError(message)


def flash_form_errors(form, category="warning"):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)
