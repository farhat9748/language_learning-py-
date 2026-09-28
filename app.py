
import os
import sys

from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager

# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# =========================================================
# DATABASE / MODEL
# =========================================================

from model import db, User


# =========================================================
# BLUEPRINTS
# =========================================================

from route.main import main_bp
from route.auth import auth_bp


# Optional admin blueprint
try:
    from route.admin import admin_bp
except Exception:
    admin_bp = None


# Optional language blueprint
try:
    from route.language import language_bp
except Exception:
    language_bp = None


# =========================================================
# CREATE FLASK APPLICATION
# =========================================================

app = Flask(
    __name__,
    template_folder="template"
)


# =========================================================
# CONFIGURATION
# =========================================================

app.config["SECRET_KEY"] = "language-learning-secret-key-2026"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" +
    os.path.join(BASE_DIR, "language_learning.db")
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

db.init_app(app)


# =========================================================
# FLASK LOGIN
# =========================================================

login_manager = LoginManager()

login_manager.init_app(app)

# If a protected page requires login,
# Flask will send the user to /auth/login
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):

    try:
        return User.query.get(int(user_id))
    except Exception:
        return None


# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(main_bp)

app.register_blueprint(auth_bp)


if admin_bp is not None:
    app.register_blueprint(admin_bp)


if language_bp is not None:
    app.register_blueprint(language_bp)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

with app.app_context():
    db.create_all()


# =========================================================
# ROOT URL
# =========================================================

@app.route("/")
def index():

    return redirect(url_for("main.home"))


# =========================================================
# START LEARNING
# =========================================================

@app.route("/start/<language>")
def start_learning(language):

    language = language.capitalize()

    return render_template(
        "index.html",
        page="start_learning",
        language=language
    )


# =========================================================
# PAYMENT
# =========================================================

@app.route("/pay/<language>")
def pay_language(language):

    language = language.capitalize()

    return render_template(
        "index.html",
        page="payment",
        language=language
    )


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "index.html",
        page="404"
    ), 404


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       LANGUAGE LEARNING SYSTEM")
    print("==========================================")
    print()
    print("Open this address in your browser:")
    print()
    print("http://127.0.0.1:5000/")
    print()
    print("==========================================")
    print()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )

