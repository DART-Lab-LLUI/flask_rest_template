from flask import Blueprint
from flask_restful import Api

bp = Blueprint('api_auth', __name__)
api_bp = Api(bp)

from server.auth import routes
from server.auth import utils
