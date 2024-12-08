from datetime import timedelta

from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.backend.routes import User, MOCK_ADMIN

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

MOCK_USER_DB = {
    '1': MOCK_ADMIN  # Key is user_id as string
}

# User Loader function
@login_manager.user_loader
def load_user(user_id):
    """Load a user from the mock database."""
    user_data = MOCK_USER_DB.get(user_id)
    if user_data:
        user = User(user_data['id'], user_data['username'])
        return user
    return None

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config['SECRET_KEY'] = 'secret_key_here'
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=0)

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adoption_center.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register your blueprint
    from .routes import main
    app.register_blueprint(main)

    # Import models and create tables
    with app.app_context():
        from app.models import User, Animal  # Import the models
        db.create_all()  # Create all tables if they don't exist

    return app
