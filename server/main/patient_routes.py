from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from server.auth.decorator import role_required
from server.extensions import db
from server.models.main import Patient

from server.main import bp


@bp.route('/patient/', methods=['GET'])
@jwt_required()
@role_required(["user"])
def get_all_patients():
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])


@bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
@role_required(["user"])
def get_patient_by_id(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return patient.to_dict()


@bp.route('/patient/', methods=['PUT'])
@jwt_required()
@role_required(["user"])
def add_patient():
    data = request.get_json()
    new_patient = Patient(**data)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify(new_patient.to_dict()), 201
