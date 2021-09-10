import os

from flask_migrate import upgrade
from flask_testing import TestCase

from foss_library.app import create_app, db

os.environ["FLASK_ENV"] = "testing"
os.environ["TESTING"] = "1"


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        with create_app().app_context():
            upgrade()

    @classmethod
    def tearDownClass(cls):
        with create_app().app_context():
            db.drop_all()
            db.engine.execute("DROP TABLE alembic_version")

    def create_app(self):
        return create_app()

    def setUp(self):
        upgrade()

    def tearDown(self):
        db.session.commit()
        db.session.remove()
