import re
from datetime import datetime, date, timedelta

def format_number(value):
    """
    Formats large numbers into human-readable compact strings (e.g., 1200 -> 1.2k).
    """
    if value is None:
        return "0"
    try:
        val = int(value)
        if val >= 1_000_000:
            return f"{val / 1_000_000:.1f}M"
        if val >= 1_000:
            return f"{val / 1_000:.1f}k"
        return str(val)
    except (ValueError, TypeError):
        return "0"


def calculate_progress_percentage(completed_count, total_count):
    """
    Calculates completion percentage safely without division-by-zero errors.
    """
    if not total_count or total_count <= 0:
        return 0
    percentage = (completed_count / total_count) * 100
    return min(100, round(percentage))


def format_minutes_to_time(minutes):
    """
    Converts estimated learning minutes into a formatted string (e.g., 65 -> '1h 5m').
    """
    if not minutes or minutes <= 0:
        return "0m"
    hours = minutes // 60
    remaining_mins = minutes % 60
    if hours > 0:
        return f"{hours}h {remaining_mins}m" if remaining_mins > 0 else f"{hours}h"
    return f"{remaining_mins}m"


def is_streak_active(last_activity_date):
    """
    Checks if a user's daily streak is still active based on their last activity date.
    Returns True if last activity was today or yesterday.
    """
    if not last_activity_date:
        return False
    if isinstance(last_activity_date, datetime):
        last_activity_date = last_activity_date.date()
    
    today = date.today()
    return (today - last_activity_date).days <= 1


def sanitize_input(text):
    """
    Strips dangerous characters and extra whitespace from user text input.
    """
    if not text:
        return ""
    # Strip HTML tags
    clean_text = re.sub(r'<[^>]*>', '', str(text))
    return clean_text.strip()


def register_template_helpers(app):
    """
    Registers utility functions directly into Jinja2 environment context filters.
    Allows use in templates like: {{ 1250|format_number }} or {{ minutes|format_time }}
    """
    app.jinja_env.filters['format_number'] = format_number
    app.jinja_env.filters['format_time'] = format_minutes_to_time
    app.jinja_env.filters['progress_pct'] = calculate_progress_percentage