from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource, fields, marshal_with, reqparse

from server.auth import bp, api_bp
from server.auth.utils import _create_refresh_token, _create_access_token
from server.extensions import db
from server.models.auth import User, RefreshToken

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

login_fields = {'access_token': fields.String, 'refresh_token': fields.String}
refresh_fields = {'access_token': fields.String}


class LoginApi(Resource):
    @marshal_with(login_fields)
    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args.username).first()
        if user is None or not user.verify_password(args.password):
            bp.logger.info("Invalid username or password")
            return jsonify({"msg": "Bad username or password"}), 401
        refresh_token, dbo = _create_refresh_token(user)
        access_token = _create_access_token(dbo)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    @marshal_with(refresh_fields)
    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt()
        refresh_token = RefreshToken.query.filter_by(jti=identity['jti']).first()
        access_token = _create_access_token(refresh_token)
        return {'access_token': access_token}

    @jwt_required(refresh=True)
    def delete(self):
        jti = get_jwt()["jti"]
        refresh_token = RefreshToken.query.filter_by(jti=jti).first()
        refresh_token.blocked = True
        db.session.commit()
        return {"msg": "Access token revoked"}


api_bp.add_resource(LoginApi, '/')
