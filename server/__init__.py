from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

from server.config import Config
import server.extensions as extensions
from server.models.auth import Role, User


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)

    # Initialize local configs in environment

    app.config.from_object(config_class)

    # Initialize Flask extensions
    extensions.db.init_app(app)
    extensions.login_manager = LoginManager(app)  # flask-login extension for user-management authentication
    extensions.login_manager .login_view = 'user_mng.login'
    extensions.jwt = JWTManager(app)  # flask-jwt-extended extension for REST authentication

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


    # simple request to install database
    @app.route('/init')
    def init_database():
        # Create Database
        extensions.db.create_all()

        # Add initial user data
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        extensions.db.session.add(admin_role)
        extensions.db.session.add(user_role)

        admin = User(username='admin', password='1234')
        admin.roles.append(admin_role)
        user = User(username='user', password='1234')
        user.roles.append(user_role)
        both = User(username='both', password='1234')
        both.roles.append(admin_role)
        both.roles.append(user_role)
        extensions.db.session.add(admin)
        extensions.db.session.add(user)
        extensions.db.session.add(both)

        extensions.db.session.commit()

        return jsonify({"message": "Database initialized"})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
