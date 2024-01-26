from datetime import datetime

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_scheduler import Scheduler

import server.extensions as extensions
from server.config import Config
from server.models.auth import Role, User, RefreshToken, AccessToken


def create_app() -> Flask:
    app = Flask(__name__)

    # Initialize local configs in environment
    app.config.from_object(Config)
    # Initialize Flask extensions
    extensions.db.init_app(app)
    extensions.migration = Migrate(app, extensions.db)
    extensions.login_manager = LoginManager(app)  # flask-login extension for user-management authentication
    extensions.login_manager.login_view = 'user_mng.login'
    extensions.jwt = JWTManager(app)
    extensions.scheduler = Scheduler(app)
    # flask-jwt-extended extension for REST authentication

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

    # Schedule delete tokens
    @extensions.scheduler.runner()
    def clear_expired_tokens():
        with app.app_context():
            expired_tokens = RefreshToken.query.filter(RefreshToken.expire_date < datetime.utcnow().timestamp()).all()
            expired_tokens += AccessToken.query.filter(AccessToken.expire_date < datetime.utcnow().timestamp()).all()
            for expired_token in expired_tokens:
                extensions.db.session.delete(expired_token)

            extensions.db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
