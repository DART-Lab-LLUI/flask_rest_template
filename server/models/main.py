from flask_restful import fields, reqparse

from server.extensions import db
from server.utils import parse_timestamp, format_timestamp


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(68))
    measures = db.relationship('Measure', backref='category')

    @classmethod
    def get_fields(cls) -> dict:
        return {"id": fields.Integer,
                "name": fields.String}


class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marker = db.Column(db.String(68))
    value = db.Column(db.Float)
    _timestamp = db.Column(db.Float)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    @property
    def timestamp(self):
        return format_timestamp(self._timestamp)

    @timestamp.setter
    def timestamp(self, timestamp_str):
        self._timestamp = parse_timestamp(timestamp_str)

    @classmethod
    def get_fields(cls) -> dict:
        return {"id": fields.Integer,
                "marker": fields.String,
                "value": fields.String,
                "timestamp": fields.String,
                "appointment_id": fields.Integer,
                "category": fields.Nested(Category.get_fields())}


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    _date = db.Column(db.Double)
    measures = db.relationship('Measure', backref='appointment')

    @property
    def date(self):
        return format_timestamp(self._date)

    @date.setter
    def date(self, date_str):
        self._date = parse_timestamp(date_str)

    @classmethod
    def get_fields(cls) -> dict:
        return {
            'id': fields.Integer,
            'patient_id': fields.Integer,
            'date': fields.String,
            'measures': fields.List(fields.Nested(Measure.get_fields()))
        }


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(68))
    surname = db.Column(db.String(68))
    _birthday = db.Column(db.Double)
    comments = db.Column(db.Text)
    appointments = db.relationship('Appointment', backref='patient')

    @property
    def birthday(self):
        if self._birthday:
            return format_timestamp(self._birthday)
        else:
            return None

    @birthday.setter
    def birthday(self, date_str: str):
        if not date_str is None:
            self._birthday = parse_timestamp(date_str)

    def __repr__(self):
        return f'<Patient "{self.id}">'

    @classmethod
    def get_fields(cls) -> dict:
        return {
            'id': fields.Integer,
            'name': fields.String,
            'birthday': fields.String,
            'surname': fields.String,
            'comments': fields.String,
            'appointments': fields.List(fields.Nested(Appointment.get_fields()))
        }

    @classmethod
    def get_parser(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('birthday', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('comments', type=str)
        return parser
