from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from server.auth import bp
from server.models.auth import User

@bp.route('/', methods=['POST'])
def login():
    username = str(request.json.get("username", None))
    password = str(request.json.get("password", None))
    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)



