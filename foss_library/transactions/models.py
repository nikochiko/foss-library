from datetime import datetime

from foss_library.database import CRUDMixin, db


class Transaction(db.Model, CRUDMixin):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey("books.id", ondelete="SET NULL"), nullable=False)
    book = db.relationship("Book", backref="transactions")
    member_id = db.Column(
        db.ForeignKey("members.id", ondelete="SET NULL"), nullable=False
    )
    member = db.relationship("Member", backref="transactions")
    borrowed_at = db.Column(db.DateTime, default=db.func.now())
    returned_at = db.Column(db.DateTime, nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @property
    def is_completed(self):
        """
        Is this transaction completed? i.e. has this book been returned
        """
        # if book has been returned, then returned_at will have some value
        return self.returned_at is not None

    @property
    def dues(self):
        """
        The dues for a transaction.

        Either returned_at - borrowed_at, if book is returned,
        or now() - borrowed_at, if book is unreturned
        """
        if self.is_completed:
            time_since_borrowed = self.returned_at - self.borrowed_at
        else:
            time_since_borrowed = datetime.now() - self.borrowed_at

        days_since_borrowed = time_since_borrowed.days
        dues_until_now = days_since_borrowed * self.book.rent_per_day

        return dues_until_now

    def return_book_and_pay_dues(self):
        """
        Complete the transaction - with returning of book and payment of dues

        Wrapped in a separate method because a few operations need to be done:
        * Set returned_at to now
        * Add amount due to member.dues_paid
        """
        if self.is_completed:
            readable_returned_at = self.returned_at.strftime("%d %B, %Y")
            raise Exception(f"Book has already been returned on {readable_returned_at}")

        dues_paid_now = self.dues
        total_dues_paid_by_member = self.member.dues_paid + dues_paid_now

        # not committing directlyy because we want both of the next updates
        # to be part of a single transaction (for atomicity)
        self.member.update(dues_paid=total_dues_paid_by_member, commit=False)
        self.update(returned_at=db.func.now(), commit=False)
        db.session.add(self.member, self)
        db.session.commit()
