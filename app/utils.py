from flask import session, redirect, url_for, jsonify
from functools import wraps

def login_required(f):
    """Decorator to protect routes and ensure the user is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):  # Check if user_id exists in session
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def logout_user():
    """Clear the session to log out the user."""
    session.pop('user_id', None)
    session.pop('user_name', None)
