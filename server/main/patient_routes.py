from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, fields, marshal_with, reqparse

from server.auth.decorator import role_required
from server.extensions import db
from server.main import api_bp
from server.models.main import Patient

patient_list_fields = {'patients': fields.List(fields.Nested(Patient.get_fields()))}

patients_parser = reqparse.RequestParser()


class PatientApi(Resource):
    @jwt_required()
    @role_required(["user"])
    @marshal_with(Patient.get_fields())
    def put(self, user_id):
        parser = Patient.get_parser()
        args = parser.parse_args()
        patient = Patient.query.get_or_404(user_id)
        patient.name = args['name'] or patient.name
        patient.surname = args['surname'] or patient.surname
        patient.birthday = args['birthday'] or patient.birthday
        patient.comments = args['comments'] or patient.comments
        db.session.commit()
        return patient

    @jwt_required()
    @role_required(["user"])
    @marshal_with(Patient.get_fields())
    def get(self, user_id):
        patient = Patient.query.get_or_404(user_id)
        return patient

    @jwt_required()
    @role_required(["user"])
    def delete(self, user_id):
        patient = Patient.query.get_or_404(user_id)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'message': 'Patient deleted'})


class PatientListApi(Resource):
    @jwt_required()
    @role_required(["user"])
    @marshal_with(patient_list_fields)
    def get(self):
        patients = Patient.query.all()
        return {'patients': patients}

    @jwt_required()
    @role_required(["user"])
    @marshal_with(Patient.get_fields())
    def post(self):
        args = Patient.get_parser().parse_args()
        patient = Patient(**args)
        db.session.add(patient)
        db.session.commit()
        return patient


api_bp.add_resource(PatientApi, '/patient/<user_id>')
api_bp.add_resource(PatientListApi, '/patient/')
