from math import ceil

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import desc

from .models import Transaction

blueprint = Blueprint("transactions", __name__, url_prefix="/transactions", static_folder="../static")


@blueprint.route("/", methods=("GET",))
def list_transactions():
    transactions_on_each_page = 20

    page = request.args.get("page", 1)
    page = int(page)

    total_pages = ceil(Transaction.query.count() / transactions_on_each_page)
    if page > total_pages:
        flash(f"Page {page} is out of range", "warning")

    limit = transactions_on_each_page
    offset = (page - 1) * transactions_on_each_page

    transactions = Transaction.query.order_by(desc(Transaction.updated_at)).limit(limit).offset(offset).all()

    return render_template("transactions/list_transactions.html", transactions=transactions, current_page=page, total_pages=total_pages)


@blueprint.route("/<int:id>/show", methods=("GET",))
def show_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return render_template("transactions/show_transaction.html", transaction=transaction)


@blueprint.route("/<int:id>/return_book", methods=("POST",))
def return_book(id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.is_completed:
        flash("Book has already been returned", "warning")
        return redirect(url_for("transactions.show_transaction", id=id))

    transaction.return_book_and_pay_dues()
    flash("Book has been returned successfully", "success")
    return redirect(url_for("transactions.show_transaction", id=id))
