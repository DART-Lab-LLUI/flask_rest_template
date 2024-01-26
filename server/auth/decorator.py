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
            has_required_role = False
            if user.roles:
                for role in user.roles:
                    if role.name in roles:
                        has_required_role = True

            if has_required_role:
                return f(*args, **kwargs)
            else:
                return abort(403)

        return decorated_function

    return decorator
