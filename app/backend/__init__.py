from datetime import timedelta

from flask_login import LoginManager
from flask import Flask, redirect, url_for

from app.backend.routes import User, MOCK_ADMIN

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
        # user.is_authenticated = True
        return user
    return None


def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config['SECRET_KEY'] = 'secret_key_here'
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=0)
    # Initialize Login Manager
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('main.not_logged_in'))

    # Register your blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
