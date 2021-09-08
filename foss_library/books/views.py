from math import ceil

from flask import Blueprint, flash, redirect, render_template, request
from sqlalchemy import desc

from foss_library.utils import flash_form_errors
from .forms import CreateBookForm, UpdateBookForm
from .models import Book

blueprint = Blueprint("books", __name__, url_prefix="/books", static_folder="../static")


@blueprint.route("/", methods=("GET",))
def list_books():
    """List books"""
    books_on_each_page = 20

    total_pages = ceil(Book.query.count() / books_on_each_page)

    # get page from request args, e.g. /books?page=1
    page = request.args.get("page", 1)
    page = int(page)

    if page > total_pages:
        flash(f"Page {page} is out of range", "error")
        return redirect("/books/")

    # set limit and offset for SQL query
    limit = books_on_each_page
    offset = (page - 1) * books_on_each_page

    books = Book.query.order_by(desc(Book.created_at)).limit(limit).offset(offset).all()
    return render_template("books/list_books.html", books=books, current_page=page, total_pages=total_pages)


@blueprint.route("/create", methods=("GET", "POST"))
def create_book():
    """Create a new book"""
    form = CreateBookForm()
    if form.validate_on_submit():
        book = Book()
        form.populate_obj(book)
        book.save()
        flash("Book created successfully!", "success")
        return redirect("/books/")

    flash_form_errors(form)
    return render_template("books/create_book.html", form=form)

@blueprint.route("/update/<int:id>", methods=("GET", "POST"))
def update_book(id):
    """Update an existing book"""
    book = Book.query.get(id)
    if book is None:
        return render_template("404.html"), 404

    form = UpdateBookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        book.save()
        flash("Book updated successfully!", "success")
        return redirect("/books/")

    flash_form_errors(form)
    return render_template("books/update_book.html", form=form)
