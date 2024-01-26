import os
from datetime import timedelta

import pytz


# This class inherits configs for the flask instance
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'you-will-never-guess'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=float(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')) or 0.1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=float(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES')) or 0.2)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///:memory:"'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_INTERVAL = int(os.environ.get('SCHEDULER_API_INTERVAL') or 5)
