from sqlalchemy import event

from server.extensions import format_timestamp, parse_timestamp, format_date, parse_date, db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(68))
    measures = db.relationship('Measure', backref='category')

    def to_dict(self) -> dict:
        return {"id": self.id,
                "name": self.name}


class Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marker = db.Column(db.String(68))
    value = db.Column(db.Float)
    _timestamp = db.Column(db.DateTime)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    @property
    def timestamp(self):
        return format_timestamp(self._timestamp)

    @timestamp.setter
    def timestamp(self, timestamp_str):
        self._timestamp = parse_timestamp(timestamp_str)

    def to_dict(self) -> dict:
        return {"id": self.id,
                "marker": self.marker,
                "value": self.value,
                "timestamp": self.timestamp,
                "appointment_id": self.appointment_id,
                "category": self.category.to_dict()}


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    _date = db.Column(db.Date)
    measures = db.relationship('Measure', backref='appointment')

    @property
    def date(self):
        return format_date(self._date)

    @date.setter
    def date(self, date_str):
        self._date = parse_date(date_str)

    def to_dict(self) -> dict:
        return {"id": self.id,
                "patient_id": self.patient_id,
                "date": self.date,
                "measures": [measure.to_dict() for measure in self.measures]}


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(68))
    surname = db.Column(db.String(68))
    _birthday = db.Column(db.Date)
    comments = db.Column(db.Text)
    appointments = db.relationship('Appointment', backref='patient')

    @property
    def birthday(self):
        return format_date(self._birthday)

    @birthday.setter
    def birthday(self, date_str: str):
        self._birthday = parse_date(date_str)

    def __repr__(self):
        return f'<Patient "{self.id}">'

    def to_dict(self) -> dict:
        return {"id": self.id,
                "name": self.name,
                "surname": self.surname,
                "birthday": self.birthday,
                "comments": self.comments,
                "appointments": [appointment.to_dict() for appointment in self.appointments]}


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
