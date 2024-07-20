import click
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    password = mapped_column(String, nullable=False)  # never do this. this is bad.


db = SQLAlchemy(model_class=Base)


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
