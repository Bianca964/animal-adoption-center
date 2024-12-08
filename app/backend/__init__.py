from datetime import timedelta
from flask import Flask, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from app.models import db, User, Animal

# Initialize the extensions (only once, don't repeat)
# db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
# User Loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database."""
    user = User.query.get(int(user_id))  # Assuming you have a User model in your database
    if user:
        return user
    return None

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

    # Configuration
    app.config['SECRET_KEY'] = 'secret_key_here'  # Change this key to something more secure in production
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=0)  # Set the duration for remember cookie
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Database URI (SQLite, can be switched)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for efficiency

    # Initialize the extensions with the app instance
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('main.not_logged_in'))

    # Register the blueprint for routes (ensure the 'main' blueprint exists)
    from .routes import main
    app.register_blueprint(main)

    return app


def init_cli_commands(app):
    """Register CLI commands with Flask."""
    from flask.cli import with_appcontext

    @app.cli.command('create-db')
    @with_appcontext
    def create_db():
        """Create the database tables."""
        db.create_all()
        print("Database created!")

    @app.cli.command('seed-db')
    @with_appcontext
    def seed_db():
        """Seed the database with sample data."""
        sample_animal = Animal(
            name="Buddy",
            age=3,
            animal_type="Dog",
            description="Friendly golden retriever",
            image="static/uploads/sample.jpg"
        )
        db.session.add(sample_animal)
        db.session.commit()
        print("Database seeded!")
