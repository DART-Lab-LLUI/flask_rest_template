from flask import Blueprint

bp = Blueprint('api_auth', __name__)

from server.auth import routes
