from datetime import datetime

from flask import Flask, has_request_context, request
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_scheduler import Scheduler

import server.extensions as extensions
from server.config import Config
from server.models.auth import Role, User, RefreshToken, AccessToken
from server.models.log import AccessLog
from server.utils import get_current_user


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)

    # Initialize local configs in environment
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    # Init all
    init_extensions(app)
    register_blueprints(app)
    init_schedules(app)
    init_access_log(app)

    return app


# Initialize Flask extensions
def init_extensions(app):
    extensions.db.init_app(app)
    extensions.migration = Migrate(app, extensions.db)
    extensions.login_manager = LoginManager(app)  # flask-login extension for user-management authentication
    extensions.login_manager.login_view = 'user_mng.login'
    extensions.jwt = JWTManager(app)
    extensions.scheduler = Scheduler(app)


def register_blueprints(app):
    # Register blueprints for different modules
    # user-management web page
    from server.user_mng import bp as user_mng_bp
    app.register_blueprint(user_mng_bp, url_prefix='/')
    # user login apis
    from server.auth import bp as api_auth_bp
    app.register_blueprint(api_auth_bp, url_prefix='/api/auth')
    # patient apis
    from server.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/api')


def init_access_log(app):
    @app.after_request
    def log_after_request(response):
        url = "Not available"
        remote_addr = "Not available"
        method = "Not available"
        if has_request_context():
            url = request.url
            remote_addr = request.remote_addr
            method = request.method
        current_user = get_current_user()
        status_code = response.status_code
        access_log = AccessLog(path=url,
                               remote_addr=remote_addr,
                               response_code=status_code,
                               username=current_user,
                               method=method)
        extensions.db.session.add(access_log)
        extensions.db.session.commit()
        return response


def init_schedules(app):
    # Schedule delete tokens
    @extensions.scheduler.runner(interval=60)
    def clear_expired_tokens():
        with app.app_context():
            expired_tokens = RefreshToken.query.filter(RefreshToken.expire_date < datetime.utcnow().timestamp()).all()
            expired_tokens += AccessToken.query.filter(AccessToken.expire_date < datetime.utcnow().timestamp()).all()
            for expired_token in expired_tokens:
                extensions.db.session.delete(expired_token)

            extensions.db.session.commit()


if __name__ == '__main__':
    app_current = create_app()
    app_current.run(debug=True)
