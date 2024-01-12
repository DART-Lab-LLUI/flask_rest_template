from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

from server.config import Config
from server.extensions import db
from server.models.auth import Role, User


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)

    # Initialize local configs in environment

    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager = LoginManager(app)  # flask-login extension for user-management authentication
    login_manager.login_view = 'user_mng.login'
    JWTManager(app)  # flask-jwt-extended extension for REST authentication

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

    # This function is needed for flask-login to retrieve a user after login
    @login_manager.user_loader
    def load_user(user_id):
        print(user_id)
        return User.query.get(int(user_id))

    # simple request to install database
    @app.route('/init')
    def init_database():
        # Create Database
        db.create_all()

        # Add initial user data
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add(admin_role)
        db.session.add(user_role)

        admin = User(username='admin', password='1234')
        admin.roles.append(admin_role)
        user = User(username='user', password='1234')
        user.roles.append(user_role)
        both = User(username='both', password='1234')
        both.roles.append(admin_role)
        both.roles.append(user_role)
        db.session.add(admin)
        db.session.add(user)
        db.session.add(both)

        db.session.commit()

        return jsonify({"message": "Database initialized"})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)