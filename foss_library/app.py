from flask import Flask

from foss_library import books, members #, transactions
from foss_library.extensions import csrf_protect, db, migrate


def create_app(config_object="foss_library.settings"):
    """App factory for our Flask app"""
    app = Flask("foss_library")
    app.config.from_object(config_object)

    # initialize extensions
    csrf_protect.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # initialize blueprints
    app.register_blueprint(books.views.blueprint)
    app.register_blueprint(members.views.blueprint)
    # app.register_blueprint(transactions.views.blueprint)

    return app
