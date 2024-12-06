from flask_login import LoginManager
from flask import Flask

from app.backend.routes import User

login_manager = LoginManager()

# User Loader function
@login_manager.user_loader
def load_user(user_id):
    # For simplicity, mock a user return
    if user_id == '1':  # Mock admin user for testing
        return User(user_id)
    return None


def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config['SECRET_KEY'] = 'secret_key_here'

    # Initialize Login Manager
    login_manager.init_app(app)

    # Register your blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
