from math import ceil

from flask import flash, render_template, request
from wtforms.validators import ValidationError


class UniqueCheck:
    def __init__(self, message=None):
        if not message:
            message = "%(modelname)s with %(fieldname)s %(fieldvalue)s already exists"

        self.message = message

    def __call__(self, form, field):
        if not hasattr(form, "_model"):
            raise Exception("Expected form to have a _model attribute")

        if (
            form._model.query.filter_by(**{field.name: field.data}).limit(1).count()
            == 1
        ):
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


def get_pagination_params_from_request_args():
    """
    Gets the pagination params (page, per_page) from
    the query params and returns them as a tuple.
    """
    # page, per_page will be defined in query params, e.g. /books?page=1
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 20)

    # request args are interpreted as str by default
    print(type(page))  # DEBUG
    page = int(page)
    per_page = int(per_page)

    return page, per_page


def validate_page(page, results):
    """
    Validates page and renders a 404 response in case it is invalid
    """
    if page < 1:
        return render_template("404.html", 404)

    if page > 1 and len(results) == 0:
        return render_template("404.html", 404)


def validate_per_page(per_page):
    """
    Validates per page and renders a 404 response in case it is invalid
    """
    if per_page < 1:
        return render_template("404.html", 404)


def paginate_query_or_404(query, page, per_page):
    """
    Paginates a query using SQL `limit` and `offset`
    Returns only the objects for that page

    Returns a 404 response if no objects were found
    for that page and page is not 1
    """
    page, per_page = get_pagination_params_from_request_args()

    # we want to fetch `per_page` results (limit)
    limit = per_page
    # and exclude the first `page - 1' pages (offset)
    offset = (page - 1) * per_page

    books = query.limit(limit).offset(offset)
    total_books = query.count()
    total_pages = ceil(total_books / per_page)

    validate_page(page, books)
    validate_per_page(per_page)

    return render_template(
        "reports/most_popular_books_report.html",
        most_popular_books=books,
        page=page,
        total_pages=total_pages,
        total_count=total_books,
    )
