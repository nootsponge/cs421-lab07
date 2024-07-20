from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

from lab07.models import User, db


bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():
    # if user is in session pass to template
    user = None
    if "user_id" in session:
        user = db.session.query(User).get(session.get("user_id"))

    return render_template("index.html", user=user)


@bp.route("/login", methods=["GET"])
def login():
    if "user_id" in session:
        flash("Already logged in")
        return redirect(url_for("main.index"))
    return render_template("login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    user = db.session.query(User).filter_by(email=email, password=password).first()
    if not user:
        flash("Invalid email or password")
        return redirect(url_for("main.login"))

    session["user_id"] = user.user_id  # never do this. this is bad.
    flash("Logged in")
    return redirect(url_for("main.secretpage"))


@bp.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    flash("Logged out")
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET"])
def register():
    if "user_id" in session:
        flash("Already logged in")
        return redirect(url_for("main.index"))
    return render_template("register.html")


@bp.route("/register", methods=["POST"])
def register_post():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]

    # ensure email not already used
    user = db.session.query(User).filter_by(email=email).first()
    if user:
        flash("Email address already exists")
        return redirect(url_for("main.register"))

    new_user = User(
        first_name=first_name, last_name=last_name, email=email, password=password
    )
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful")
    return redirect(url_for("main.thankyou"))


@bp.route("/secretpage", methods=["GET"])
def secretpage():
    if "user_id" not in session:
        flash("Must be logged in to view this page")
        return redirect(url_for("main.login"))

    user = db.session.query(User).get(session.get("user_id"))
    if not user:
        flash("Must be logged in to view this page")
        return redirect(url_for("main.login"))

    return render_template("secretpage.html", user=user)


@bp.route("/thankyou", methods=["GET"])
def thankyou():
    users = db.session.query(User).all()
    return render_template("thankyou.html", users=users)
