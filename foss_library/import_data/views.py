from flask import Blueprint, flash, render_template

from foss_library.books.models import Book
from foss_library.utils import flash_form_errors
from .forms import ImportDataForm
from .frappe_api import get_n_books_from_api

blueprint = Blueprint(
    "import_data", __name__, url_prefix="/import", static_folder="../static"
)


@blueprint.route("/", methods=("GET", "POST"))
async def import_data():
    """
    Async view for importing data. Async so that the program can
    run fast and exit before the HTTP request times out
    """
    form = ImportDataForm()

    if form.validate_on_submit():
        count = form.count.data
        title = form.title.data
        authors = form.authors.data
        isbn = form.isbn.data
        publisher = form.publisher.data

        total_results = 0
        added_count = 0
        duplicates_count = 0

        async for book in get_n_books_from_api(
            count, title=title, authors=authors, isbn=isbn, publisher=publisher
        ):
            total_results += 1

            # TODO: add book to DB, on conflict do nothing
            # figure out how to do it with SQLAlchemy
            if Book.query.get(book.id) is None:
                book.save()
                added_count += 1
            else:
                duplicates_count += 1

        if total_results == 0:
            flash("No results found for given search params", "danger")
        else:
            flash(
                f"Got {total_results} results from API. Imported {added_count} books, {duplicates_count} were duplicates",
                "success",
            )

        return render_template("import_data/import_data.html", form=form)

    flash_form_errors(form)
    return render_template("import_data/import_data.html", form=form)
