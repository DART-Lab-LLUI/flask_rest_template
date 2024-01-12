from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from server.auth.decorator import role_required
from server.extensions import db
from server.models.main import Appointment
from server.main import bp



@bp.route('/appointment/<int:appointment_id>', methods=['GET'])
@jwt_required()
@role_required("user")
def get_appointment_by_id(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return appointment.to_dict()


@bp.route('/appointment/', methods=['PUT'])
@jwt_required()
@role_required("user")
def add_appointment():
    data = request.get_json()
    new_appointment = Appointment(**data)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(new_appointment.to_dict()), 201
