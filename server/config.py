import os

basedir = os.path.abspath(os.path.dirname(__file__))


# This class inherits configs for the flask instance
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "test"
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "amazingsecretkey"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
