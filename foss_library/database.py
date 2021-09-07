from foss_library.extensions import db


class CRUDMixin(object):
    """
    Mixin that adds convenience methods for CRUD (create, read, update, delete) operations.

    From: flask-cookiecutter
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def get_or_create(cls, **kwargs):
        """Get an object with the given kwargs from DB, or create one"""
        instance = cls.query.filter_by(**kwargs).first()
        if instance:
            return instance

        return cls.create(**kwargs)

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            return db.session.commit()
        return
