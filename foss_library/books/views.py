from math import ceil

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import desc

from foss_library.database import db
from foss_library.exceptions import FOSSLibraryBaseException
from foss_library.utils import flash_form_errors
from foss_library.members.models import Member
from foss_library.transactions.models import Transaction
from .forms import (
    InitiateBookReturnForm,
    IssueBookForm,
    CreateBookForm,
    SearchBookForm,
    UpdateBookForm,
)
from .models import Book

blueprint = Blueprint("books", __name__, url_prefix="/books", static_folder="../static")


def filter_books_by_request_args():
    title = request.args.get("title")
    author = request.args.get("author")

    filters = []

    if title:
        title = title.lower()
        filters.append(db.func.lower(Book.title).like(f"%{(title)}%"))

    if author:
        author = author.lower()
        filters.append(db.func.lower(Book.authors).like(f"%{author}%"))

    return Book.query.filter(*filters)


@blueprint.route("/", methods=("GET",))
def list_books():
    """List books"""
    books_on_each_page = 20

    # get page from request args, e.g. /books?page=1
    page = request.args.get("page", 1)
    page = int(page)

    # set limit and offset for SQL query
    limit = books_on_each_page
    offset = (page - 1) * books_on_each_page

    books_query = filter_books_by_request_args()
    books = books_query.limit(limit).offset(offset).all()

    total_pages = ceil(books_query.count() / books_on_each_page)

    if page > 1 and page > total_pages:
        flash(f"Page {page} is out of range", "warning")

    search_form = SearchBookForm(request.args)

    return render_template(
        "books/list_books.html",
        books=books,
        current_page=page,
        total_pages=total_pages,
        search_form=search_form,
    )


@blueprint.route("/create", methods=("GET", "POST"))
def create_book():
    """Create a new book"""
    form = CreateBookForm()
    if form.validate_on_submit():
        book = Book()
        form.populate_obj(book)
        book.save()
        flash("Book created successfully!", "success")
        return redirect(url_for("books.list_books"))

    search_form = SearchBookForm(request.args)

    flash_form_errors(form)
    if form.errors:
        status_code = 400
    else:
        status_code = 200

    return (
        render_template("books/create_book.html", form=form, search_form=search_form),
        status_code,
    )


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
        return redirect(url_for("books.list_books"))

    search_form = SearchBookForm(request.args)

    flash_form_errors(form)
    if form.errors:
        status_code = 400
    else:
        status_code = 200

    return (
        render_template(
            "books/update_book.html", book=book, form=form, search_form=search_form
        ),
        status_code,
    )


@blueprint.route("/delete/<int:id>", methods=("POST",))
def delete_book(id):
    """Delete a book"""
    book = Book.query.get(id)
    if book is None:
        return render_template("404.html"), 404

    book.delete()
    flash("Book deleted successfully!", "success")
    return redirect(url_for("books.list_books"))


@blueprint.route("/show/<int:id>", methods=("GET",))
def show_book(id):
    """Show a book"""
    book = Book.query.get_or_404(id)

    issue_form = IssueBookForm(obj=book)
    return_form = InitiateBookReturnForm(obj=book)
    search_form = SearchBookForm(request.args)

    members = Member.query.all()
    issue_form.member_id.choices = [(m.id, m.name) for m in members]

    return render_template(
        "books/show_book.html",
        book=book,
        issue_form=issue_form,
        return_form=return_form,
        search_form=search_form,
    )


@blueprint.route("/issue/<int:id>", methods=("POST",))
def issue_book(id):
    """Issue a book"""
    book = Book.query.get_or_404(id)

    form = IssueBookForm(obj=book)
    if form.validate_on_submit():
        member_id = form.member_id.data
        member = Member.query.get(member_id)
        if member is None:
            flash(
                f"Member with ID {member_id} doesn't exist. Please check your input",
                "warning",
            )
            return redirect(url_for("books.show_book", id=id))

        try:
            book.issue_to(member)
        except FOSSLibraryBaseException as e:
            flash(str(e), "danger")
            return redirect(url_for("books.show_book", id=id))

        flash("Book has been issued", "success")
        return redirect(url_for("books.show_book", id=id))

    flash_form_errors(form)
    return redirect(url_for("books.show_book", id=id))


@blueprint.route("/initiate_return/<int:id>", methods=("POST",))
def initiate_book_return(id):
    """Initiate a book return"""
    book = Book.query.get_or_404(id)

    form = InitiateBookReturnForm(obj=book)
    if form.validate_on_submit():
        member_id = form.member_id.data
        member = Member.query.get(member_id)
        if member is None:
            flash(
                f"Member with ID {member_id} doesn't exist. Please check your input",
                "warning",
            )
            return redirect(url_for("books.show_book", id=id)), 400

        txn = Transaction.query.filter_by(
            member=member, book=book, returned_at=None
        ).first()
        if txn is None:
            flash(f"Member with ID {member_id} hasn't borrowed this book.")
            return redirect(url_for("books.show_book", id=id)), 400

        return redirect(url_for("transactions.show_transaction", id=txn.id)), 400

    else:
        flash_form_errors(form)
        if form.errors:
            status_code = 400
        else:
            status_code = 200

        return redirect(url_for("books.show_book", id=id)), status_code
