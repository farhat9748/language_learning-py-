from flask import Blueprint, render_template
from model import db, User  # Only import what exists


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def admin_dashboard():
    # Simple admin page - customize as needed
    return render_template("index.html", page="admin")