from functools import wraps
from typing import List

from flask import abort
from flask_jwt_extended import get_jwt_identity
from server.models.auth import User


def role_required(roles: List):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.get(current_user)
            if not user.roles or any(role in user.roles for role in roles):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
