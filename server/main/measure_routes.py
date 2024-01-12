from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from server.auth.decorator import role_required
from server.extensions import db
from server.models.main import Measure

from server.main import bp


@bp.route('/measure/', methods=['GET'])
@jwt_required()
@role_required("user")
def get_all_measures():
    measures = Measure.query.all()
    return jsonify([measure.to_dict() for measure in measures])


@bp.route('/measure/<int:measure_id>', methods=['GET'])
@jwt_required()
@role_required("user")
def get_measure_by_id(measure_id):
    measure = Measure.query.get_or_404(measure_id)
    return measure.to_dict()


@bp.route('/measure/', methods=['PUT'])
@jwt_required()
@role_required("user")
def add_measure():
    data = request.get_json()
    new_measure = Measure(**data)
    db.session.add(new_measure)
    db.session.commit()
    return jsonify(new_measure.to_dict()), 201


@bp.route('/measure/<int:measure_id>', methods=['DELETE'])
@jwt_required()
@role_required("user")
def delete_measure(measure_id):
    measure = Measure.query.get_or_404(measure_id)
    db.session.delete(measure)
    db.session.commit()
    return jsonify({"message", f"Measure {measure_id} deleted"}), 200
