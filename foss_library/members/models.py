from foss_library.database import CRUDMixin, db


class Member(db.Model, CRUDMixin):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    dues_paid = db.Column(db.Integer, default=0, index=True)

    # timestamps
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
