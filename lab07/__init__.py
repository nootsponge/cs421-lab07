import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///database.sqlite",
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import models

    models.init_app(app)

    from . import routes

    app.register_blueprint(routes.bp)

    return app
