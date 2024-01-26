from datetime import datetime

from flask import g


def get_current_user():
    user = g.get("_jwt_extended_jwt_user")
    current_user = "Anonymous"
    if user is None:
        user = g.get("_login_user")
    else:
        user = user["loaded_user"]

    if not user is None:
        current_user = user.username

    return current_user


def parse_timestamp(timestamp_str: str) -> float:
    return datetime.fromisoformat(timestamp_str).timestamp()


def format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()
