import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


# This class inherits configs for the flask instance
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "test"
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "amazingsecretkey"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 6)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=os.environ.get('JWT_REFRESH_TOKEN_EXPIRES') or 30)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
