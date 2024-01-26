from datetime import datetime

from server.extensions import db


class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(36), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(36), nullable=False)
    response_code = db.Column(db.Integer, nullable=False)
    remote_addr = db.Column(db.String(36), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
