from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = None
login_manager = None
scheduler = None

