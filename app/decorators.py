from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def superadmin_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            
            if not current_user.is_superadmin:
                return redirect(url_for("main.index"))
        
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
