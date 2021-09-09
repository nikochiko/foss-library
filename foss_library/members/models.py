from foss_library.database import CRUDMixin, db
from foss_library.transactions.models import Transaction


MAX_OUTSTANDING_DUES = 500


class Member(db.Model, CRUDMixin):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    dues_paid = db.Column(db.Integer, default=0, index=True)

    # timestamps
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @property
    def outstanding_dues(self):
        """Outstanding dues of this member"""
        txns = Transaction.query.filter_by(
            member_id=self.id, returned_at=None,
        ).all()
        return sum(txn.dues for txn in txns)

    @property
    def can_borrow_new_book(self):
        return self.outstanding_dues <= 500
