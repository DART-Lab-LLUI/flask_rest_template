from flask import Blueprint

bp = Blueprint('patient', __name__)

from server.main import appointment_routes, measure_routes, patient_routes

