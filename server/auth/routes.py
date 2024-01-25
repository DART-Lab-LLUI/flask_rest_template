import datetime
from datetime import datetime

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, decode_token, \
    get_jwt

from server.auth import bp
from server.extensions import db, jwt
from server.models.auth import User, RefreshToken, AccessToken


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    jwt_type = jwt_payload["type"]
    refresh_token = None
    if jwt_type == "access":
        refresh_token = AccessToken.query.filter_by(jti=jti).first().refresh_token
    elif jwt_type == "refresh":
        refresh_token = RefreshToken.query.filter_by(jti=jti).first()

    print(refresh_token.blocked)
    return refresh_token is None or refresh_token.blocked


def _create_refresh_token(user: User) -> [str, RefreshToken]:
    refresh_token = create_refresh_token(identity=user.id)
    decoded = decode_token(refresh_token)
    refresh_token_dbo = RefreshToken(jti=decoded['jti'],
                                     blocked=False,
                                     user_id=user.id,
                                     expire_date=datetime.fromtimestamp(decoded['exp']))

    db.session.add(refresh_token_dbo)
    db.session.commit()
    return refresh_token, refresh_token_dbo


def _create_access_token(refresh_token: RefreshToken) -> str:
    access_token = create_access_token(identity=refresh_token.user_id)
    decoded = decode_token(access_token)
    access_token_dbo = AccessToken(jti=decoded['jti'],
                                   refresh_token=refresh_token,
                                   expire_date=datetime.fromtimestamp(decoded['exp']))

    db.session.add(access_token_dbo)
    db.session.commit()
    return access_token


@bp.route('/login', methods=['POST'])
def login():
    username = str(request.json.get("username", None))
    password = str(request.json.get("password", None))
    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    refresh_token, dbo = _create_refresh_token(user)
    access_token = _create_access_token(dbo)

    return jsonify(access_token=access_token, refresh_token=refresh_token)


@bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt()
    refresh_token = RefreshToken.query.filter_by(jti=identity['jti']).first()
    access_token = _create_access_token(refresh_token)
    return jsonify(access_token=access_token)


@bp.route("/logout", methods=["DELETE"])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]
    refresh_token = RefreshToken.query.filter_by(jti=jti).first()
    refresh_token.blocked = True
    db.session.commit()
    return jsonify(msg="Access token revoked")
