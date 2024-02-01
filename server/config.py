import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    PROPAGATE_EXCEPTIONS = os.environ.get("PROPAGATE_EXCEPTIONS", True)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    # How long an authorization is valid (in minutes)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=float(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
    # How login an refresh is valid (in days)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=float(os.getenv("JWT_REFRESH_TOKEN_EXPIRES")))

    # Database uri
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")