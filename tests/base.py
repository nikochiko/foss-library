import os

from flask_migrate import upgrade
from flask_testing import TestCase

from foss_library.app import create_app, db

os.environ["FLASK_ENV"] = "testing"
os.environ["TESTING"] = "1"


class BaseTest(TestCase):
    def create_app(self):
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.commit()
        db.session.remove()

        db.drop_all()
