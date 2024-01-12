from functools import wraps

from flask import abort
from flask_jwt_extended import get_jwt_identity
from server.models.auth import User


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.get(current_user)
            if not user.has_role(role):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
