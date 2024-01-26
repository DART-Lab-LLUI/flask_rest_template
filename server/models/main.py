from flask_restful import fields, reqparse
from sqlalchemy import event

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


# generate data on creation of table
@event.listens_for(Category.__table__, 'after_create')
def create_category(*args, **kwargs):
    db.session.add(Category(name='HR'))
    db.session.add(Category(name='Blood Pressure'))
    db.session.commit()


@event.listens_for(Patient.__table__, 'after_create')
def create_patient(*args, **kwargs):
    patient = Patient(name='Luca', surname='Nastasi', birthday='11.07.1997', comments="cool Dude")
    db.session.add(patient)
    db.session.commit()


@event.listens_for(Appointment.__table__, 'after_create')
def create_appointment(*args, **kwargs):
    patient = Appointment(date='1.1.2024', patient_id=1)
    db.session.add(patient)
    db.session.commit()


@event.listens_for(Measure.__table__, 'after_create')
def create_measure(*args, **kwargs):
    measure1 = Measure(timestamp="1.1.2024 11:00:00.112",
                       value=59,
                       marker="heart",
                       category_id=1,
                       appointment_id=1)

    measure2 = Measure(timestamp="1.1.2024 11:00:00.112",
                       value=61,
                       marker="heart",
                       category_id=1,
                       appointment_id=1)
    db.session.add(measure1)
    db.session.add(measure2)
    db.session.commit()
