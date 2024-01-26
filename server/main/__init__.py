from flask import Blueprint
from flask_restful import Api

bp = Blueprint('patient', __name__)
api_bp = Api(bp)

from server.main import patient_routes

