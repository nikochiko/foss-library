from sqlalchemy import func

from foss_library.database import CRUDMixin, db


class Transaction(db.Model, CRUDMixin):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey("books.id"), nullable=False)
    book = db.relationship("Book", backref="transactions")
    member_id = db.Column(db.ForeignKey("members.id"), nullable=False)
    member = db.relationship("Member", backref="transactions")
    borrowed_at = db.Column(db.DateTime, default=func.now())
    returned_at = db.Column(db.DateTime, nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
