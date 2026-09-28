
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from model import db, User


# =========================================================
# AUTH BLUEPRINT
# =========================================================

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Empty fields
        if not email or not password:

            flash(
                "Please enter email and password.",
                "error"
            )

            return render_template(
                "index.html",
                page="login"
            )

        # Find user
        user = User.query.filter_by(
            email=email
        ).first()

        # Check password
        if user and user.check_password(password):

            login_user(user)

            flash(
                "Login successful!",
                "success"
            )

            return redirect(
                url_for("main.home")
            )

        # Invalid login
        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "index.html",
        page="login"
    )


# =========================================================
# REGISTER
# =========================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    # Already logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # Required fields
        if not name or not email or not password:

            flash(
                "All fields are required.",
                "error"
            )

            return render_template(
                "index.html",
                page="register"
            )

        # Password confirmation
        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return render_template(
                "index.html",
                page="register"
            )

        # Minimum password length
        if len(password) < 6:

            flash(
                "Password must be at least 6 characters.",
                "error"
            )

            return render_template(
                "index.html",
                page="register"
            )

        # Check existing email
        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return render_template(
                "index.html",
                page="register"
            )

        # Create new user
        user = User(
            name=name,
            email=email
        )

        # Password hash
        user.set_password(password)

        db.session.add(user)

        db.session.commit()

        flash(
            "Registration successful! Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "index.html",
        page="register"
    )


# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route("/logout")
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("main.home")
    )
