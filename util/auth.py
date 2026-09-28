from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user

def login_required_custom(f):
    """
    Custom decorator to protect routes that require user authentication.
    Redirects unauthenticated users to the login page with a warning flash message.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def guest_only(f):
    """
    Decorator to restrict access to guest-only routes (e.g., login, registration).
    Redirects authenticated users to the main dashboard.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """
    Utility function to retrieve the currently active user instance.
    Returns None if the user is unauthenticated.
    """
    if current_user.is_authenticated:
        return current_user
    return None


def calculate_user_level(total_xp):
    """
    Calculates user level based on total XP points earned.
    Every 100 XP grants 1 Level.
    """
    if not total_xp or total_xp < 0:
        return 1
    return (total_xp // 100) + 1