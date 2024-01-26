from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from server.auth import bp
from server.auth.utils import _create_refresh_token, _create_access_token
from server.extensions import db
from server.models.auth import User, RefreshToken


@bp.route('/', methods=['POST'])
def login():
    username = str(request.json.get("username", None))
    password = str(request.json.get("password", None))
    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        bp.logger.info("Invalid username or password")
        return jsonify({"msg": "Bad username or password"}), 401

    refresh_token, dbo = _create_refresh_token(user)
    access_token = _create_access_token(dbo)

    return jsonify(access_token=access_token, refresh_token=refresh_token)


@bp.route("/", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt()
    refresh_token = RefreshToken.query.filter_by(jti=identity['jti']).first()
    access_token = _create_access_token(refresh_token)
    return jsonify(access_token=access_token)


@bp.route("/", methods=["DELETE"])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]
    refresh_token = RefreshToken.query.filter_by(jti=jti).first()
    refresh_token.blocked = True
    db.session.commit()
    return jsonify(msg="Access token revoked")
