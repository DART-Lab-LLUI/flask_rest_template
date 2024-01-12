from flask import Blueprint

bp = Blueprint('user_mng', __name__)

from server.user_mng import routes