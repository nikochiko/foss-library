from flask import Flask, render_template

from foss_library import books, import_data, members, public, reports, transactions
from foss_library.extensions import csrf_protect, db, flask_static_digest, migrate


def not_found_error(e):
    return render_template("404.html"), 404


def create_app(config_object="foss_library.settings"):
    """App factory for our Flask app"""
    app = Flask("foss_library")
    app.config.from_object(config_object)

    # initialize extensions
    csrf_protect.init_app(app)
    db.init_app(app)
    flask_static_digest.init_app(app)
    migrate.init_app(app, db)

    # register custom error handler
    app.register_error_handler(404, not_found_error)

    # initialize blueprints
    app.register_blueprint(books.views.blueprint)
    app.register_blueprint(import_data.views.blueprint)
    app.register_blueprint(members.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(reports.views.blueprint)
    app.register_blueprint(transactions.views.blueprint)

    return app
