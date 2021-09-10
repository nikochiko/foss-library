from math import ceil

from flask import Blueprint, flash, render_template, request

from foss_library.database import db
from foss_library.books.models import Book
from foss_library.transactions.models import Transaction


blueprint = Blueprint(
    "reports", __name__, url_prefix="/reports", static_folder="../static"
)


def get_most_popular_books_query():
    most_popular_books_query = (
        Book.query.join(Transaction, Book.id == Transaction.book_id)
        .add_columns(db.text(f"count({Transaction.__tablename__}.id) as popularity"))
        .order_by(db.text("popularity desc"))
        .group_by(Book.id)
    )
    return most_popular_books_query


@blueprint.route("/")
def list_reports():
    return render_template("reports/list_reports.html")


@blueprint.route("/most-popular-books")
def most_popular_books_report():
    on_each_page = 20

    # get page from request args, e.g. /books?page=1
    page = request.args.get("page", 1)
    page = int(page)

    # set limit and offset for SQL query
    limit = on_each_page
    offset = (page - 1) * on_each_page

    most_popular_books_query = get_most_popular_books_query()
    most_popular_books = most_popular_books_query.limit(limit).offset(offset).all()

    total_pages = ceil(most_popular_books_query.count() / on_each_page)

    if page > total_pages:
        flash(f"Page {page} is out of range", "warning")

    return render_template(
        "reports/most_popular_books_report.html",
        most_popular_books=most_popular_books,
        current_page=page,
        total_pages=total_pages,
        offset=offset,
    )


@blueprint.route("/highest-paying-customers")
def highest_paying_customers_report():
    return "hello"
