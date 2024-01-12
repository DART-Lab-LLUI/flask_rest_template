from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from server.extensions import db

user_role = db.Table('user_role',
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary=user_role, backref='users')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name: str) -> bool:
        for role in self.roles:
            if role.name == role_name:
                return True
        return False
