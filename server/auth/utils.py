from datetime import datetime

from flask_jwt_extended import create_refresh_token, decode_token, create_access_token

from server import AccessToken, RefreshToken, User
from server.extensions import jwt, db

@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    jwt_type = jwt_payload["type"]
    refresh_token = None
    if jwt_type == "access":
        refresh_token = AccessToken.query.filter_by(jti=jti).first().refresh_token
    elif jwt_type == "refresh":
        refresh_token = RefreshToken.query.filter_by(jti=jti).first()

    return refresh_token is None or refresh_token.blocked


def _create_refresh_token(user: User) -> [str, RefreshToken]:
    refresh_token = create_refresh_token(identity=user)
    decoded = decode_token(refresh_token)
    refresh_token_dbo = RefreshToken(jti=decoded['jti'],
                                     blocked=False,
                                     user_id=user.id,
                                     expire_date=datetime.fromtimestamp(decoded['exp']).timestamp())

    db.session.add(refresh_token_dbo)
    db.session.commit()
    return refresh_token, refresh_token_dbo


def _create_access_token(refresh_token: RefreshToken) -> str:
    access_token = create_access_token(identity=refresh_token.user)
    decoded = decode_token(access_token)
    access_token_dbo = AccessToken(jti=decoded['jti'],
                                   refresh_token=refresh_token,
                                   expire_date=datetime.fromtimestamp(decoded['exp']).timestamp())

    db.session.add(access_token_dbo)
    db.session.commit()
    return access_token
